import os
import time
from src.config import Settings
import torch.multiprocessing as mp
from src.utils.singleton import singleton
from datetime import datetime

from torch.profiler import profile, record_function, ProfilerActivity


# Class derived from LlmWorkerBase will be instantiated in a child process.
# This class initializes the model in the way you specify.
# To interact with an instance of this class you can use the LlmProcessDescriptor class.
# In order to run some task, you should define a method, and then pass it into a child process:
# 
# class WorkerClass:
#   ...
#   def method_name(params):
#       param1, param2 = params
#       ... 
# 
# processDescriptorInstance.execute(workerClassInstance.method_name, params)
# 
class LlmWorkerBase:
    tokenizer = None
    model = None
    generation_pipeline = None
    model_id: str = None
    cache_dir = Settings().models_cache_dir

    def initialize_model():
        raise NotImplementedError("Method initialize_model should be defined in a derived class")

# This class is an interface between parent process and single child process
# Instance of this class contains data of a single child process. 
# This is class serves single child process and can be accessed from the parent process. 
# Instance of this class can be created by LlmManager.
class LlmProcessDescriptor(object):
    # TODO: worker_init_params should be a pydantic class derived from BaseModel, for more clear parameters specifictation
    def __init__(self, name, worker_class, worker_init_params):
        self.name = name
        self.worker_class = worker_class
        self.task_queue = mp.Queue()
        self.result_queue = mp.Queue()

        # Running separate process for model
        self.process = mp.Process(
            target=worker_process,
            args=(self.worker_class, worker_init_params, self.task_queue, self.result_queue)
        )
        self.process.start()
    
    # This method runs in a parent process and puts method and params into a task queue.
    # Provided method with it's params will be executed in a child process.
    # Execution result will be retrieved from the result queue and returned from execute method in a parent process.
    async def execute(self, method, params):
        start_time = time.time()

        # Отправляем текст в очередь задач
        self.task_queue.put((method, params))
        
        # Получаем результат из очереди результатов
        result = self.result_queue.get()

        print("--- %s seconds ---" % (time.time() - start_time))
        return result


# This class creates child processes and stores ther descriptors for communication.
@singleton
class LlmManager(object):
    worker_descriptors_list = []

    # This method creates a process and corresponding process descriptor which allowes to interact with this process.
    def create_process(self, worker_class, worker_init_params):
        if (not issubclass(worker_class, LlmWorkerBase)): 
            raise TypeError(f"{worker_class.__name__} should be a child of {LlmWorkerBase.__name__}")

        # TODO: add labels for process names. Inside of the name or separately - up to you
        process_name = f"{worker_class.__name__}_{self.worker_descriptors_list.count(worker_class.__name__)}"
        self.worker_descriptors_list.append(LlmProcessDescriptor(process_name, worker_class, worker_init_params))
        print(f"Created process: {process_name}")

    # This method provides worker descriptor which you can interact with 
    def get_worker(self, name: str):
        for worker_descriptor in self.worker_descriptors_list:
            if worker_descriptor.name == name:
                return worker_descriptor
        else:
            raise KeyError(f"No worker with name {name}")

    def shutdown(self):
        self.task_queue.put(None)  # Сигнал остановки для процесса
        self.process.join()

# This method runs inside of the child process awaiting for new execution requests.
# This method puts execution results into a result_queue, and then they can be retrieved from it in a parent process.
def worker_process(worker_class, worker_init_params, task_queue, result_queue):
    worker_instance = worker_class(worker_init_params)
    worker_instance.initialize_model()
    
    while True:
        # Получаем задачу из очереди
        task = task_queue.get()
        if task is None:
            break  # Завершаем процесс, если получен сигнал остановки

        method, params = task
        result = method(worker_instance, params)
                
        # Отправляем результат обратно в очередь результатов
        result_queue.put(result)
# PureBPMN
A fully asynchronous and configurable Business Process Management Framework Built in Bare Metal Python

# What is this?

- Fully asynchronous framework
- The business process flow is through configuration, **not code**
- Multi-threading at a model level than system level
- Inherently thread safe concurrent execution even for code that is written with no concurrency control. (See the calculator example below).
- Written with native python modules and no external module dependency.
- The entire bootstrapped model resides in the cache.
- Configurable thread-safe loggers with no blocking I/O.

# What are the building blocks?

- Queues
- Threads
- Semaphores
- Events
- Cached classes and methods
- Logger
- ConfigParser

# How to implement a calculator with this framework?

![image](https://user-images.githubusercontent.com/27330002/26960273-1f61ab56-4c93-11e7-8e1a-b397e45e9fc1.png)

## config/calculator.conf

```
[model]
keys=connection,input,add,print,subtract

These all the models that we see in the flowchart. 
Connection is a system model, others are user models.

[model_input]
type=generator => The model is a generator which means it one that produces only output and does not have any inputs.
module=calculator => The user model is defined in the module calculator.py
class=calculator => The user model is defined in the class calculator in module calculatory.py
method=input => The user model is defined in the method input in class calculator.
OnSuccess=add,subtract => The models to which the outputs of this model to be sent.
OnFailure=
thread_pool_max=90 => Max threads for running the model
thread_count=1 => No. of parallel threads this model will be run in. Eg: If the generator is having 2 threads, 2 models will be instantiated and executed thread safe.
queue_count=10 => Don't care to set it for generators.
input_ports= => Don't care to set it for generators.

[model_add]
type=transfer => The model is transfer type which means it has both input and output queues. 
module=calculator 
class=calculator
method=add => The method which corresponds to the user defined model add in the flowchart.
OnSuccess=print => The output of the add model is sent to print model. This is the default behavior.
OnFailure= => If you want to have a different flow for success and failure conditions in the model, you can set to the next user defined model incase of a failure condiiton. (None for this example).
thread_pool_max=90 => Only max 90 threads can run even though thread_count is defined as 100 below.
thread_count=100 => There are 100 instances of add model that will run in parallel. Each model can have its own setting. Parallelism is defined at the model level instead of system level.
queue_count=10 => The number of input queues this model will listen to. So when the model is instantiated it will have 10 input queues. The connection system model will take care of distributing the outputs of the predecessor model to the input queues. So, here, the model input doesn't need to know how many queues are available for a write.
input_ports=any => If the model depends on inputs from more than one user defined model, this tells whether this model should wait for all predecessors' output. Here it is only one, hence any or all doesn't make any difference.

[model_subtract]
... => Same as model_add

[model_print]
type=sink => The model is a sink which means it (the/one of the) final models where the flow terminates.
module=calculator
class=calculator
method=print
OnSuccess=
OnFailure=
thread_pool_max=90
thread_count=100
queue_count=1
input_ports=all => Specified as all, which means the model will wait for both add and subtract models to produce an output before it will execute. 
```

## calculator.py

    def input(self,resultQ,*args,**kwargs): => This is the default signature of every method that the user model implements. The resultQ is injected when the model is instantiated.
        for i in range(1000):
            self._a = random.randint(0,9999)
            self._b = random.randint(0,9999)
            resultQ.put({'value1':self._a,'value2':self._b}) => This is how you will output a value of a model. 

    def add(self,resultQ,*args,**kwargs):
        self._result = kwargs.get('value1') + kwargs.get('value2') => This is how you get the inputs of the model. If input of this model is dependent on multiple models, those outputs are automatically merged into kwargs, so that you have to just remember one way of getting the value.
        resultQ.put({'op':'add','value1':kwargs.get('value1'),'value2':kwargs.get('value2'),'op1':self._result})

subtract and print methods are very similar.
Never call methods representing the model directly. It will defeat the statelessness of the framework and produce undesirable results.

# How to run?

`python ModelStart.py calculator.conf`

# What's the output?


```
2017-06-09 06:23:27,715: ModelBootstrap : INFO    : Thread-1   : Starting Threads
2017-06-09 06:23:27,934: ModelBootstrap : INFO    : Thread-1   : Started all Threads.
{'value1': 5915, 'op1': 10411, 'value2': 1831, 'op': 'sub'}
{'value1': 5915, 'value2': 1831, 'op': 'sub', 'op2': 4084}
{'value1': 9452, 'op1': 12778, 'value2': 3532, 'op': 'sub'}

```

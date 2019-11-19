
from abc import ABCMeta, abstractmethod
import datetime


STATUS_COMPLETE = "complete"
STATUS_ACTIVE = "active"
STATUS_TODO = "todo"
STATUS_HOLD = "hold"
STATUS_DISCARDED = "discarded"


class BaseProject(metaclass=ABCMeta):
    '''
    The tasks should be sortable by basically all its attributes; due
    date, priority, date created, start date, estimated time, etc.

    The order of the tasks

    The project should also be able to apply the filter and limit the
    number of tasks shown.
    '''

    # fn: archive project

    @abstractmethod
    def __init__(self, name, status=STATUS_ACTIVE):
        self.tasks = {}
        self.name = name
        self.status = status
        self.created = datetime.datetime.now()
        self.updated = datetime.datetime.now()
        self.next_task_pid = 0

    def __repr__(self):
        return f'Project(name={self.name})'

    def assign_task_pid(self, t):
        t.pid = self.next_task_pid
        pid = self.next_task_pid
        self.next_task_pid += 1
        return pid

    def add_task(self, task):
        pid = self.assign_task_pid(task)
        self.tasks[pid] = task
        return pid

    def update_task(self, pid, updated_task):
        if not self.tasks.get(pid, None):
            raise IndexError(f'task with pid {pid} does not exist.')
        self.tasks[pid] = updated_task

    def delete_task(self, pid):
        deleted_t = self.tasks.pop(pid, None)
        if deleted_t is None:
            raise IndexError(f'task with pid {pid} does not exist.')

        moved_tasks = {k - 1: task for k, task in self.tasks.items()
                       if k > pid}
        pruned_tasks = {k: task for k, task in self.tasks.items() if k < pid}
        self.tasks = {**pruned_tasks, **moved_tasks}


class ArcProject(BaseProject):
    '''
    ArcProject projects end. They involve a series of tasks that, once
    complete, results in the completion of the project.
    '''

    def __init__(self, name, due=None, status=STATUS_ACTIVE):
        super().__init__(name, status)
        self.due = due


class CycleProject(BaseProject):
    '''
    CycleProject projects don't end. They involve recurring, scheduled
    tasks that are meant to be completed on a regular basis.
    '''

    def __init__(self, name, status=STATUS_ACTIVE):
        super().__init__(name, status)


class Task:
    '''
    Each task needs to have an ID unique to the project
    '''

    def __init__(self, name, notes=None, start=None, due=None, est=None,
                 status=STATUS_TODO, project=None):
        '''if project is None, the task is uncategorized'''
        self.name = name
        self.notes = notes
        self.start = None
        self.due = None
        self.est = None
        self.status = status
        self.project = project
        self.priority = 0
        self.pid = 0

    def __repr__(self):
        return f'Task(name={self.name})'


def test():
    p = ArcProject('test_proj')
    print(p)

    t0 = Task('task0')
    t1 = Task('task1')
    t2 = Task('task2')
    t3 = Task('task3')
    t4 = Task('task4')

    p.add_task(t0)
    p.add_task(t1)
    p.add_task(t2)
    p.add_task(t3)
    p.add_task(t4)
    print(p.tasks)


if __name__ == '__main__':
    test()

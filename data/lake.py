import os
import h5py
import pytest
from typing import Tuple
from numpy.typing import ArrayLike
from abc import ABC, abstractmethod

# class ETL(ABC):

    # def __init__(self, *args):
    #     pass

    # def _validate(func, *args, **kwargs):
    #     def _execute(self, *args, **kwargs):
    #         if not self.file:
    #             self.file = self.__init__(self.name,)
    #         try:
    #             return func(self, *args, **kwargs)
    #         except:
    #             self.file.close()
    #             print(f'{func.__name__} failed to execute.')
    #     return _execute

    # @abstractmethod

class Lake:
    def __init__(self, name: str, mode: str='a'):
        self.name = name
        self.mode = mode
        self.file = h5py.File(f'{name}.h5', mode)
    
    def _validate(func, *args, **kwargs):
        def _execute(self, *args, **kwargs):
            if self.file.__str__() == '<Closed HDF5 file>':
                self.file = h5py.File(f'{self.name}.h5', self.mode)
            try:
                return func(self, *args, **kwargs)
            except:
                self.file.close()
                print(f'{func.__name__} failed to execute.')
        return _execute

    @_validate
    def write(self, key: str, content: Tuple[list, ArrayLike]) -> None:
        assert self.mode in ['r+', 'w', 'w-', 'x', 'a'], f'{self.name} is not in a valid write mode.'
        headers, dataset = content
        self.file[key] = dataset
        self.file[key].fields = headers
    
    @_validate
    def read(self, key: str) -> h5py.Dataset:
        assert self.mode in ['r', 'r+', 'a'], f'{self.name} is not in a valid read mode.'
        return self.file[key]

    @_validate
    def update(self, key: str, content: Tuple[list, ArrayLike]) -> None:
        headers, dataset = content
        self.file[key].fields = headers
        self.file[key][:] = dataset
    
    @_validate
    def delete(self, key: str, verify = True) -> None:
        assert self.file[key], f'{self.name} has no attribute: {key}'
        if verify:
            print('Are you sure you want to delete {key}? Type "proceed" to proceed.\n')
            proceed = input()
        else:
            proceed = True
        while proceed:
            _dir, target = os.path.split(key)
            group = self.file[_dir]
            group.__delitem__(target)
            if len(group.parent[_dir]) == 0:
                key = _dir
                continue
            else:
                break

    def fetch_file(self) -> h5py.File:
        return self.file
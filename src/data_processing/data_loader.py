"""
数据加载和处理的基础类
提供统一的数据处理接口
"""
from abc import ABC, abstractmethod
import pandas as pd
from pathlib import Path
from typing import Dict, Any, Optional, List

class DataLoader(ABC):
    """数据加载的基类"""
    
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self.data = None
        
    @abstractmethod
    def load(self) -> pd.DataFrame:
        """加载数据的抽象方法"""
        pass
    
    @abstractmethod
    def preprocess(self) -> pd.DataFrame:
        """预处理数据的抽象方法"""
        pass
    
    def get_data(self) -> pd.DataFrame:
        """获取处理后的数据"""
        if self.data is None:
            self.data = self.load()
            self.data = self.preprocess()
        return self.data

class CSVLoader(DataLoader):
    """CSV文件加载器"""
    
    def __init__(self, file_path: str, **kwargs):
        super().__init__(file_path)
        self.kwargs = kwargs
    
    def load(self) -> pd.DataFrame:
        return pd.read_csv(self.file_path, **self.kwargs)
    
    def preprocess(self) -> pd.DataFrame:
        # 在这里实现具体的预处理逻辑
        return self.data

class ExcelLoader(DataLoader):
    """Excel文件加载器"""
    
    def __init__(self, file_path: str, sheet_name: Optional[str] = None, **kwargs):
        super().__init__(file_path)
        self.sheet_name = sheet_name
        self.kwargs = kwargs
    
    def load(self) -> pd.DataFrame:
        return pd.read_excel(self.file_path, sheet_name=self.sheet_name, **self.kwargs)
    
    def preprocess(self) -> pd.DataFrame:
        # 在这里实现具体的预处理逻辑
        return self.data
"""
数据集成管理器
用于管理和集成多个数据源
"""
from typing import Dict, List, Optional
import pandas as pd
from pathlib import Path
from .data_loader import DataLoader

class DataIntegrator:
    """数据集成管理器"""
    
    def __init__(self):
        self.data_sources: Dict[str, DataLoader] = {}
        self.integrated_data = None
        
    def add_data_source(self, name: str, loader: DataLoader):
        """添加数据源"""
        self.data_sources[name] = loader
    
    def get_data_source(self, name: str) -> Optional[pd.DataFrame]:
        """获取指定数据源的数据"""
        if name in self.data_sources:
            return self.data_sources[name].get_data()
        return None
    
    def integrate_data(self, join_keys: Dict[str, str], how: str = 'left') -> pd.DataFrame:
        """
        集成多个数据源
        join_keys: 字典，键是数据源名称，值是用于连接的列名
        how: 连接方式（'left', 'right', 'inner', 'outer'）
        """
        if not self.data_sources:
            raise ValueError("No data sources added")
            
        # 获取第一个数据源作为基础
        base_name = list(join_keys.keys())[0]
        result = self.get_data_source(base_name)
        
        # 依次与其他数据源合并
        for name in list(join_keys.keys())[1:]:
            if name in self.data_sources:
                other_data = self.get_data_source(name)
                result = pd.merge(
                    result,
                    other_data,
                    left_on=join_keys[base_name],
                    right_on=join_keys[name],
                    how=how
                )
        
        self.integrated_data = result
        return result
    
    def get_integrated_data(self) -> Optional[pd.DataFrame]:
        """获取集成后的数据"""
        return self.integrated_data
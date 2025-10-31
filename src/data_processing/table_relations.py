"""
表关系管理器
用于处理和管理数据表之间的关系
"""
from typing import Dict, List, Optional, Union
import pandas as pd
import networkx as nx
from sqlalchemy import inspect, MetaData, Table
import matplotlib.pyplot as plt
from .postgresql_loader import PostgreSQLLoader

class TableRelationManager:
    """管理数据表之间的关系"""
    
    def __init__(self, db_loader: PostgreSQLLoader):
        """
        初始化表关系管理器
        
        参数:
            db_loader: PostgreSQL加载器实例
        """
        self.db_loader = db_loader
        self.relationships = {}
        self.metadata = MetaData()
        self.graph = nx.DiGraph()
        
    def analyze_foreign_keys(self) -> Dict:
        """
        分析数据库中的外键关系
        
        返回:
            包含表之间关系的字典
        """
        inspector = inspect(self.db_loader.engine)
        relationships = {}
        
        # 获取所有表
        tables = inspector.get_table_names()
        
        # 分析每个表的外键
        for table in tables:
            foreign_keys = inspector.get_foreign_keys(table)
            if foreign_keys:
                relationships[table] = []
                for fk in foreign_keys:
                    relationships[table].append({
                        'referred_table': fk['referred_table'],
                        'constrained_columns': fk['constrained_columns'],
                        'referred_columns': fk['referred_columns']
                    })
                    
                    # 添加到图中
                    self.graph.add_edge(
                        table, 
                        fk['referred_table'],
                        columns=f"{','.join(fk['constrained_columns'])} -> {','.join(fk['referred_columns'])}"
                    )
        
        self.relationships = relationships
        return relationships
    
    def get_related_tables(self, table_name: str) -> List[Dict]:
        """
        获取与指定表直接相关的所有表
        
        参数:
            table_name: 表名
        返回:
            相关表的列表
        """
        related = []
        
        # 检查该表是否有外键引用其他表
        if table_name in self.relationships:
            for relation in self.relationships[table_name]:
                related.append({
                    'table': relation['referred_table'],
                    'type': 'references',
                    'through': f"{table_name}.{relation['constrained_columns']} -> "
                              f"{relation['referred_table']}.{relation['referred_columns']}"
                })
        
        # 检查该表是否被其他表引用
        for table, relations in self.relationships.items():
            for relation in relations:
                if relation['referred_table'] == table_name:
                    related.append({
                        'table': table,
                        'type': 'referenced_by',
                        'through': f"{table}.{relation['constrained_columns']} -> "
                                 f"{table_name}.{relation['referred_columns']}"
                    })
        
        return related
    
    def find_path_between_tables(self, source: str, target: str) -> List[str]:
        """
        找到两个表之间的关系路径
        
        参数:
            source: 源表名
            target: 目标表名
        返回:
            表名的列表，表示从源表到目标表的路径
        """
        try:
            path = nx.shortest_path(self.graph, source, target)
            return path
        except nx.NetworkXNoPath:
            return []
    
    def generate_join_query(self, source: str, target: str) -> Optional[str]:
        """
        生成连接两个表的SQL查询
        
        参数:
            source: 源表名
            target: 目标表名
        返回:
            SQL查询字符串
        """
        path = self.find_path_between_tables(source, target)
        if not path:
            return None
            
        joins = []
        select_tables = [source]
        
        for i in range(len(path) - 1):
            current = path[i]
            next_table = path[i + 1]
            
            # 找到这两个表之间的关系
            if current in self.relationships:
                for relation in self.relationships[current]:
                    if relation['referred_table'] == next_table:
                        join_condition = [
                            f"{current}.{col} = {next_table}.{ref_col}"
                            for col, ref_col in zip(
                                relation['constrained_columns'],
                                relation['referred_columns']
                            )
                        ]
                        joins.append(f"JOIN {next_table} ON {' AND '.join(join_condition)}")
                        select_tables.append(next_table)
                        break
        
        # 构建完整的查询
        select_clause = ", ".join([f"{table}.*" for table in select_tables])
        query = f"SELECT {select_clause} FROM {source} " + " ".join(joins)
        return query
    
    def visualize_relationships(self, filename: Optional[str] = None):
        """
        可视化表关系
        
        参数:
            filename: 可选的输出文件名
        """
        plt.figure(figsize=(12, 8))
        pos = nx.spring_layout(self.graph)
        
        # 绘制节点
        nx.draw(self.graph, pos, with_labels=True, node_color='lightblue', 
                node_size=2000, font_size=10, font_weight='bold')
        
        # 绘制边的标签
        edge_labels = nx.get_edge_attributes(self.graph, 'columns')
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels, font_size=8)
        
        if filename:
            plt.savefig(filename)
        plt.show()

    def execute_path_query(self, source: str, target: str) -> pd.DataFrame:
        """
        执行路径查询并返回结果
        
        参数:
            source: 源表名
            target: 目标表名
        返回:
            查询结果DataFrame
        """
        query = self.generate_join_query(source, target)
        if query:
            return self.db_loader.execute_query(query)
        return pd.DataFrame()
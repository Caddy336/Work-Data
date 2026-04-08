"""
PostgreSQL数据加载器
提供与PostgreSQL数据库的集成
"""
import pandas as pd
from sqlalchemy import create_engine, text
from typing import Optional, Dict, List, Union
class PostgreSQLLoader:
    """PostgreSQL数据加载器"""
    
    def __init__(self, 
                 host: str,
                 database: str,
                 user: str,
                 password: str,
                 port: int = 5432,
                 query: Optional[str] = None,
                 table_name: Optional[str] = None):
        """
        初始化PostgreSQL连接
        
        参数:
        - host: 数据库主机
        - database: 数据库名
        - user: 用户名
        - password: 密码
        - port: 端口号
        - query: SQL查询语句
        - table_name: 表名（如果不使用自定义查询）
        """
        self.connection_params = {
            'host': host,
            'database': database,
            'user': user,
            'password': password,
            'port': port
        }
        self.query = query
        self.table_name = table_name
        self._engine = None
        
    @property
    def engine(self):
        """获取SQLAlchemy引擎"""
        if self._engine is None:
            conn_str = f"postgresql://{self.connection_params['user']}:{self.connection_params['password']}@"\
                      f"{self.connection_params['host']}:{self.connection_params['port']}/"\
                      f"{self.connection_params['database']}"
            self._engine = create_engine(conn_str)
        return self._engine
    
    def load(self) -> pd.DataFrame:
        """从PostgreSQL加载数据"""
        if self.query:
            return pd.read_sql(text(self.query), self.engine)
        elif self.table_name:
            return pd.read_sql(f"SELECT * FROM {self.table_name}", self.engine)
        else:
            raise ValueError("必须提供query或table_name之一")
    
    def preprocess(self) -> pd.DataFrame:
        """预处理PostgreSQL数据"""
        # 在这里实现特定的预处理逻辑
        return self.data
    
    def execute_query(self, query: str) -> pd.DataFrame:
        """执行自定义SQL查询"""
        return pd.read_sql(text(query), self.engine)
    
    def list_tables(self) -> List[str]:
        """列出数据库中的所有表"""
        query = """
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
        """
        return [row[0] for row in self.engine.execute(text(query))]
    
    def get_table_schema(self, table_name: str) -> pd.DataFrame:
        """获取表结构信息"""
        query = f"""
        SELECT column_name, data_type, is_nullable
        FROM information_schema.columns
        WHERE table_name = '{table_name}'
        """
        return pd.read_sql(text(query), self.engine)
    
    def close(self):
        """关闭数据库连接"""
        if self._engine is not None:
            self._engine.dispose()
            self._engine = None
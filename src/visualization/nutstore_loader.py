"""
坚果云数据加载模块
用于通过 WebDAV 协议从坚果云加载 Excel 数据
"""
import os
import pandas as pd
from pathlib import Path
from typing import Dict, Optional
from webdav3.client import Client
import logging

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NutStoreLoader:
    """坚果云数据加载器"""
    
    def __init__(
        self, 
        email: str, 
        app_password: str, 
        hostname: str = "https://dav.jianguoyun.com/dav/"
    ):
        """
        初始化坚果云加载器
        
        参数:
            email: 坚果云账号邮箱
            app_password: 坚果云应用密码（在账户设置中生成）
            hostname: WebDAV 服务器地址
        """
        self.email = email
        self.app_password = app_password
        self.hostname = hostname
        self.client = None
        self._setup_client()
    
    def _setup_client(self):
        """设置 WebDAV 客户端"""
        try:
            options = {
                'webdav_hostname': self.hostname,
                'webdav_login': self.email,
                'webdav_password': self.app_password
            }
            self.client = Client(options)
            logger.info("✅ 成功连接到坚果云")
        except Exception as e:
            logger.error(f"❌ 连接坚果云失败: {str(e)}")
            raise ConnectionError(f"无法连接到坚果云: {str(e)}")
    
    def download_file(
        self, 
        remote_path: str, 
        local_path: Optional[str] = None
    ) -> str:
        """
        从坚果云下载文件
        
        参数:
            remote_path: 坚果云上的文件路径
            local_path: 本地保存路径（可选）
        
        返回:
            本地文件路径
        """
        if local_path is None:
            # 自动生成本地路径
            filename = os.path.basename(remote_path)
            local_path = os.path.join("data", "raw", filename)
        
        # 确保目录存在
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        
        try:
            logger.info(f"📥 正在下载: {remote_path}")
            self.client.download_sync(
                remote_path=remote_path,
                local_path=local_path
            )
            logger.info(f"✅ 文件已保存到: {local_path}")
            return local_path
        except Exception as e:
            logger.error(f"❌ 下载失败: {str(e)}")
            raise IOError(f"下载文件失败: {str(e)}")
    
    def load_excel(
        self, 
        remote_path: str, 
        sheet_names: Optional[list] = None,
        local_path: Optional[str] = None
    ) -> Dict[str, pd.DataFrame]:
        """
        从坚果云加载 Excel 文件
        
        参数:
            remote_path: 坚果云上的 Excel 文件路径
            sheet_names: 要加载的 sheet 名称列表（None 表示加载所有）
            local_path: 本地保存路径（可选）
        
        返回:
            字典 {sheet_name: DataFrame}
        """
        # 下载文件
        local_file = self.download_file(remote_path, local_path)
        
        try:
            # 读取 Excel 文件
            logger.info(f"📖 正在读取 Excel 文件...")
            excel_file = pd.ExcelFile(local_file)
            
            # 确定要读取的 sheet
            if sheet_names is None:
                sheet_names = excel_file.sheet_names
            
            # 读取所有指定的 sheet
            data_dict = {}
            for sheet_name in sheet_names:
                if sheet_name in excel_file.sheet_names:
                    logger.info(f"  📊 读取 sheet: {sheet_name}")
                    df = pd.read_excel(local_file, sheet_name=sheet_name)
                    data_dict[sheet_name] = df
                    logger.info(f"    ✅ {len(df)} 行 × {len(df.columns)} 列")
                else:
                    logger.warning(f"  ⚠️ Sheet '{sheet_name}' 不存在")
            
            logger.info(f"✅ 成功加载 {len(data_dict)} 个数据表")
            return data_dict
            
        except Exception as e:
            logger.error(f"❌ 读取 Excel 失败: {str(e)}")
            raise ValueError(f"读取 Excel 文件失败: {str(e)}")
    
    def list_files(self, remote_path: str = "") -> list:
        """
        列出坚果云指定路径下的文件
        
        参数:
            remote_path: 远程目录路径
        
        返回:
            文件列表
        """
        try:
            files = self.client.list(remote_path)
            return files
        except Exception as e:
            logger.error(f"❌ 列出文件失败: {str(e)}")
            return []
    
    def check_connection(self) -> bool:
        """
        检查连接是否正常
        
        返回:
            True 表示连接正常
        """
        try:
            self.client.list()
            return True
        except:
            return False


def load_coffee_data(email: str, app_password: str) -> Dict[str, pd.DataFrame]:
    """
    便捷函数：加载咖啡进出口数据
    
    参数:
        email: 坚果云账号
        app_password: 坚果云应用密码
    
    返回:
        包含三个 sheet 的字典
    """
    loader = NutStoreLoader(email, app_password)
    
    remote_path = "Gondwana/04_Coffee Business 咖啡业务/03 行情报告/10 Import and Price Track/Supply_Demand BS.xlsx"
    sheet_names = ['Demand_Factsheet', 'China_Import', 'China_Export']
    
    return loader.load_excel(remote_path, sheet_names)


if __name__ == "__main__":
    # 测试代码
    print("请在主应用中使用此模块")

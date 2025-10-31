"""
坚果云数据加载器和本地 CSV 加载工具
"""
import pandas as pd
import streamlit as st
from pathlib import Path


class NutStoreLoader:
    """坚果云数据加载器（内置版本，无需外部依赖）"""
    
    def __init__(self, email: str, app_password: str, hostname: str = "https://dav.jianguoyun.com/dav/"):
        """初始化坚果云加载器"""
        self.email = email
        self.app_password = app_password
        self.hostname = hostname
        self.client = None
        self._setup_client()
    
    def _setup_client(self):
        """设置 WebDAV 客户端"""
        try:
            from webdav3.client import Client
            options = {
                'webdav_hostname': self.hostname,
                'webdav_login': self.email,
                'webdav_password': self.app_password
            }
            self.client = Client(options)
        except ImportError:
            raise ImportError("需要安装 webdavclient3: pip install webdavclient3")
        except Exception as e:
            raise ConnectionError(f"无法连接到坚果云: {str(e)}")
    
    def download_file(self, remote_path: str, local_path: str) -> str:
        """从坚果云下载文件"""
        import os
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        self.client.download_sync(remote_path=remote_path, local_path=local_path)
        return local_path
    
    def load_excel(self, remote_path: str, sheet_names=None):
        """从坚果云加载 Excel 文件"""
        import tempfile
        import os
        
        # 下载到临时文件
        with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp_file:
            local_path = tmp_file.name
        
        try:
            self.download_file(remote_path, local_path)
            excel_file = pd.ExcelFile(local_path)
            
            if sheet_names is None:
                sheet_names = excel_file.sheet_names
            
            data_dict = {}
            for sheet_name in sheet_names:
                if sheet_name in excel_file.sheet_names:
                    df = pd.read_excel(local_path, sheet_name=sheet_name)
                    data_dict[sheet_name] = df
            
            return data_dict
        finally:
            # 清理临时文件
            if os.path.exists(local_path):
                os.remove(local_path)
    
    def check_connection(self) -> bool:
        """检查连接是否正常"""
        try:
            self.client.list()
            return True
        except:
            return False


def load_from_nutstore():
    """从坚果云加载数据"""
    try:
        # 尝试从 secrets 读取凭证
        if hasattr(st, 'secrets') and 'nutstore' in st.secrets:
            email = st.secrets['nutstore']['email']
            app_password = st.secrets['nutstore']['app_password']
        else:
            return None, "未配置坚果云凭证（需要在 .streamlit/secrets.toml 中配置）"
        
        # 创建加载器
        loader = NutStoreLoader(email=email, app_password=app_password)
        
        if not loader.check_connection():
            return None, "无法连接到坚果云（请检查网络和凭证）"
        
        # 加载 Excel 数据
        remote_path = "Gondwana/04_Coffee Business 咖啡业务/03 行情报告/10 Import and Price Track/Supply_Demand BS.xlsx"
        sheet_names = ['China_Import', 'Original_Export']
        
        data_sheets = loader.load_excel(remote_path=remote_path, sheet_names=sheet_names)
        
        import_data = data_sheets['China_Import'].copy()
        export_data = data_sheets['Original_Export'].copy()
        
        return (import_data, export_data), None
        
    except ImportError as e:
        return None, f"缺少依赖: {str(e)}。请运行: pip install webdavclient3"
    except Exception as e:
        return None, f"加载失败: {str(e)}"


def load_csv_data():
    """从本地 CSV 文件加载数据（备选方案）"""
    try:
        base_path = Path(__file__).parent.parent
        
        # 尝试读取 CSV 文件
        import_csv = base_path / 'monthly_import_data.csv'
        
        if import_csv.exists():
            import_data = pd.read_csv(import_csv)
            
            # 处理日期列
            if 'year' in import_data.columns and 'month' in import_data.columns:
                import_data['date'] = pd.to_datetime(
                    import_data['year'].astype(str) + '-' + 
                    import_data['month'].astype(str).str.zfill(2) + '-01'
                )
            
            return import_data, None
        else:
            return None, f"未找到数据文件: {import_csv}"
            
    except Exception as e:
        return None, f"加载本地数据失败: {str(e)}"

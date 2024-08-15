from django.test import TestCase
from data_input import foecast_info_update3, demand_info_update1
from demand_main import d_main

class DmdModelTests(TestCase):
    """
    需要予測に必要な関数を一括実行するテスト。
    """
    def test_foecast_info_update3(self):
        try:
            foecast_info_update3()
            print("foecast_info_update3:成功")
        except Exception as e:
            self.fail(f"foecast_info_update3: {e}")
    
    def test_demand_info_update1(self):
        try:
            demand_info_update1()
            print("demand_info_update1:成功")
        except Exception as e:
            self.fail(f"demand_info_update1: {e}")
    
    # def test_d_main(self):
    #     try:
    #         d_main()
    #         print("d_main:成功")
    #     except Exception as e:
    #         self.fail(f"d_main: {e}")
    
# Create your tests here.

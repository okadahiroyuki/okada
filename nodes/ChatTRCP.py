#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-
"""
    Chat program

    ROSPEEXから入力された文章を使い、DoCoMoAPIで会話する

    The project is hosted on GitHub where your could fork the project or report
    issues. Visit https://github.com/roboworks/

    :copyright: (c) 2015 by Hiroyuki Okada, All rights reserved.
    :license: MIT License (MIT), http://www.opensource.org/licenses/MIT
"""
__author__ = 'Hiroyuki Okada'
__version__ = '0.1'
import sys
import time
sys.path.append(".")
import urllib2
import urllib
import json
import rospy
from std_msgs.msg import String

from rospeex_if import ROSpeexInterface

from okada.srv import *
from okada.msg import *


class ChatTRCP(object):
    """ ChatTRCP class """
    def __init__(self):
        """ Initializer """

    def run(self):
        """ run ros node """
        # initialize ros node
        rospy.init_node('ChatTRCP')
        rospy.loginfo("start DoCoMo Chat TRCP node")
        
        """ for ROSpeexInterface """
        rospeex = ROSpeexInterface()
        rospeex.init()
        rospeex.register_sr_response( self.sr_response )

        """日本語（英語もある）でNICT(Googleもある)"""
        """launchファイ決めてもいいけど、動的に変更する？"""
        """とりあえず、現状は決め打ち"""
        self.lang = 'ja'
        self.input_engine = 'nict'        
        rospeex.set_spi_config(language='ja',engine='nict')

        """ 発話理解APIの準備 """
        self.req = DoCoMoUnderstandingReq()
        self.req.projectKey = 'OSU'    
        self.req.appName = ''
        self.req.appKey = 'hoge_app01'
        self.req.clientVer = '1.0.0'
        self.req.dialogMode = 'off'
        self.req.language = 'ja'
        self.req.userId = '12 123456 123456 0'
        self.req.lat = '139.766084'
        self.req.lon = '35.681382'


        rospy.wait_for_service('docomo_sentenceunderstanding')
        self.understanding = rospy.ServiceProxy('docomo_sentenceunderstanding',DoCoMoUnderstanding)
        rospy.wait_for_service('docomo_qa')        
        self.qa = rospy.ServiceProxy('docomo_qa',DoCoMoQa)



        rospy.spin()

    def sr_response(self, message):
        rospy.loginfo("sr_responsee:%s", message)

        try:
            # self.req.utteranceText ="富士山の高さを教えて"
            #self.req.utteranceText ="世界で一番数の多い虫は"
            self.req.utteranceText = message
            resp = self.understanding(self.req)
            if  resp.success:
                if resp.response.commandId == "BC00101":
                    """雑談"""
                    print resp.response.commandId


                elif resp.response.commandId == "BK00101":
                    """知識検索"""
                    rospy.loginfo("TRCP:Q&A")
                    self.req_qa = DoCoMoQaReq()
                    self.req_qa.text = resp.response.utteranceText
                    print resp.response.utteranceText
                    res_qa = self.qa(self.req_qa)
                    rospy.loginfo("TRCP Q&A response:%s",res_qa.response.code)
                    """
                    質問回答のレスポンスコードは、下記のいずれかを返却。
                    S020000: 内部のDBからリストアップした回答
                    S020001: 知識Q&A APIが計算した回答
                    S020010: 外部サイトから抽出した回答候補
                    S020011: 外部サイトへのリンクを回答
                    E010000: 回答不能(パラメータ不備)
                    E020000: 回答不能(結果0件)
                    E099999: 回答不能(処理エラー)
                    ※Sで始まる場合は正常回答、
                    Eで始まる場合は回答が得られていないことを示す。
                    """
                    if res_qa.success:
                        print res_qa.response.textForDisplay
                        rospy.loginfo("TRCP:%s",res_qa.response.textForSpeech)
                      # for answer in res_qa.response.answer:
                      #     print answer.rank
                      #     print answer.answerText
                      #     print answer.linkText
                      #     print answer.linkUrl
                        if res_qa.response.code == 'S020000':
                            pass
                        elif res_qa.response.code == 'S020001':
                            pass
                        elif res_qa.response.code == 'S020010':
                            pass
                        elif res_qa.response.code == 'S020011':
                            pass                            
                        elif res_qa.response.code == 'E010000':
                            pass
                        elif res_qa.response.code == 'E020000':
                            pass
                        elif res_qa.response.code == 'E099999':
                            pass
                        else:
                            pass
                    else:
                        pass

                        
                else:
                    """判定不能"""
                    """Undeterminable"""     
                    
            else:
                pass
        except:
            pass


        
#        resp = understanding(self.req)
#        print resp
        






        #
        #        try:
#            ret = self.docomo_qa(message)
#            if ret.success:
#                rospy.loginfo("DoCoMoSentenceUnderstanding Response:%s", ret.response)
#            else:
#                rospy.loginfo("DoCoMoSentenceUnderstanding Response:failed")            
#        except:
#            pass



            
if __name__ == '__main__':
    try:
        node = ChatTRCP()
        node.run()
    except rospy.ROSInterruptException:
        pass

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



        self.req.utteranceText ="富士山の高さを教えて"
        rospy.wait_for_service('docomo_sentenceunderstanding')
        understanding = rospy.ServiceProxy('docomo_sentenceunderstanding',DoCoMoUnderstanding)
        rospy.wait_for_service('docomo_qa')        
        qa = rospy.ServiceProxy('docomo_qa',DoCoMoQa)

        try:
            resp = understanding(self.req)
            if  resp.success:
                if resp.response.commandId == "BC00101":
                    """雑談"""
                    print resp.response.commandId



                elif resp.response.commandId == "BK00101":
                    print "aaaaaaaaaaaaaaaaaaa"
                    print resp.response.commandId

                    self.req_qa = DoCoMoQaReq()
                    print "aaaaaaaaaaaaaaaaaaa"
                    """知識検索"""
                    print self.req_qa
                    self.req_qa.text = resp.response.utteranceText
                    print "aaaaaaaaaaaaaaaaaaa"
                    print self.req_qa
                    print "aaaaaaaaaaaaaaaaaaa"                    
                    res_qa = qa(self.req_qa)

                    print res_qa
                else:
                    """判定不能"""
                    """Undeterminable"""     
                    
            else:
                pass
        except:
            pass

        






        rospy.spin()

    def sr_response(self, message):
        rospy.loginfo("sr_responsee:%s", message)

        rospy.wait_for_service('docomo_sentenceunderstanding')
        undersanding = rospy.ServiceProxy('docomo_sentenceunderstanding',DoCoMoUnderstanding)

        resp = understanding(self.req)
        print resp
        
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

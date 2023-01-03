import cv2
import numpy as np
from pyzbar.pyzbar import decode
import os

cap=cv2.VideoCapture(0)
cap.set(3,1080)
cap.set(4,650)

while cap.isOpened():
    ret,frame=cap.read()
    qr=decode(frame)
    for object in decode(frame):
        myData=object.data.decode('utf-8')
        # print(myData)
        txt=myData.split(";")
        password=txt[1][2:]
        id=txt[2][2:]
        security=txt[0][7:]
        # print(id)
        # print(password)

        pts=np.array([object.polygon],np.int32)
        cv2.polylines(frame,[pts],True,(255,0,0),5)
        pts2=object.rect
        cv2.putText(frame,"SSID-> "+id,(pts2[0],pts2[1]-70),cv2.FONT_HERSHEY_COMPLEX,1,(214,225,10),2)
        cv2.putText(frame,"Password-> "+password,(pts2[0],pts2[1]-40),cv2.FONT_HERSHEY_COMPLEX,1,(100,100,255),2)
        cv2.putText(frame,"Security-> "+security,(pts2[0],pts2[1]-10),cv2.FONT_HERSHEY_COMPLEX,1,(236,168,66),2)
        
        # os.system('cmd /c "netsh wlan show networks"')

        def createNewConnection(name, SSID, password):
            config = """<?xml version=\"1.0\"?>
        <WLANProfile xmlns="http://www.microsoft.com/networking/WLAN/profile/v1">
            <name>"""+name+"""</name>
            <SSIDConfig>
                <SSID>
                    <name>"""+SSID+"""</name>
                </SSID>
            </SSIDConfig>
            <connectionType>ESS</connectionType>
            <connectionMode>auto</connectionMode>
            <MSM>
                <security>
                    <authEncryption>
                        <authentication>WPA2PSK</authentication>
                        <encryption>AES</encryption>
                        <useOneX>false</useOneX>
                    </authEncryption>
                    <sharedKey>
                        <keyType>passPhrase</keyType>
                        <protected>false</protected>
                        <keyMaterial>"""+password+"""</keyMaterial>
                    </sharedKey>
                </security>
            </MSM>
        </WLANProfile>"""
            command = "netsh wlan add profile filename=\"./"+name+".xml\""+" interface=Wi-Fi"
            with open("./"+name+".xml", 'w') as file:
                file.write(config)
            os.system(command)

        # function to connect to a network
        def connect(name, SSID):
            command = "netsh wlan connect name=\""+name+"\" ssid=\""+SSID+"\" interface=Wi-Fi"
            os.system(command)

        # # function to display avavilabe Wifi networks
        # def displayAvailableNetworks():
        #     command = "netsh wlan show networks interface=Wi-Fi"
        #     os.system(command)


        # # display available netwroks
        # displayAvailableNetworks()
        name = id

        # establish new connection
        createNewConnection(name, name, password)

        # connect to the wifi network
        connect(name, name)
        
    
    cv2.imshow("Code",frame)
    if cv2.waitKey(20) & 0xFF == 27:
        break
        
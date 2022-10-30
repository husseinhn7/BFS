from collections import deque
from functools import partial
from random import randrange
from kivy.clock import Clock
from time import sleep
from kivy.config import Config
from kivy.utils import get_color_from_hex
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'width', '1200')
Config.set('graphics', 'height',  '625')
from kivymd.app import MDApp
from kivy.app import App

import threading
from kivy.uix.button import Button
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen

        
class Stor:
    head=[]
    target=[]
    def __init__(self):
        pass
    @classmethod
    def stor_head(self,value):
        Stor.head.append(value)
    @classmethod
    def stor_target(self,value):
        Stor.target.append(value)
        
class Data:
    __mkWall=False
    __wallHead=None
    __start=None
    __target=None
    def __init__(self) :
        pass
    @property
    def wallHead(self):
        return self.__wallHead
    @wallHead.setter
    def wallHead(self,value0):
        self.__wallHead=value0
    @property
    def mkWall(self):
        return self.__mkWall
    @mkWall.setter
    def mkWall(self,value0):
        self.__mkWall=value0
    @property
    def start(self):
        return self.__start
    @start.setter
    def start(self,value0):
        self.__start=value0

class BFS:
    def __init__(self,head):
        self.__head=head
    def search(self,head):
        color=1
        num=0
        search_queue=deque()
        search_queue+=head.neighbors()
        while search_queue:
            
            node=search_queue.popleft()
            
            node.background_color=[0,1,1,color]
            # node.background_normal=''
            # node.background_color=[1,1,1,1]
            if node==Stor.target[0]:
                node.draw_path()
                Stor.head.clear()
                Stor.target.clear()
                
                print(f'fond him at {node}')
                break
            else:
                ni=node.neighbors()
                search_queue+=ni
                for i in ni:
                    i.background_color=[0,1,0,1] 
            color-=0.01
            sleep(.01)
            
            num+=1
                    
class Window(Screen):
    def __init__(self,**kwargs):
        super(Window,self).__init__(**kwargs)
        self.set_window()
    def set_window(self,*args):
        self.clear_widgets()
        for i in range(48):
            for n in range(30):
                a=Node(size=(19,19),pos=(20*i+10, 20*n+10))
                self.add_widget(a)
        wall=Node(size=(100,40),pos=(1035, 60),text=f'make wall')
        wall.background_color=[1,1,1,1]
        self.add_widget(wall)
        dwall=Node(size=(100,40),pos=(1035, 10),text=f'start')
        self.add_widget(dwall)
        r=Button(size_hint=(None,None),size=(100,40),pos=(1035, 110),text=f'reset',on_press=self.set_window)
        self.add_widget(r)
    
              
class Node(Button,Data):
    __All={}
    __nodes=[]
    def __init__(self, **kwargs):
        super(Node,self).__init__(**kwargs)
        self.size_hint=(None,None)
        self.background_normal=''
        self.background_down=''
        self.background_color=[1,1,1,.5]
        self.border=(2,2,2,2)
        cord=self
        self.__wall=False
        self.__All[f'{cord}']=self
        self.__nodes.append(self)
        self.__parentNode=None
        self.wallHead=None
        
    @property
    def wallHead(self):
        return Data.wallHead
    @wallHead.setter
    def wallHead(self,value0):
        Data.wallHead=value0
    @property
    def mkWall(self):
        return Data.mkWall
    @mkWall.setter
    def mkWall(self,value0):
        Data.mkWall=value0
    @property
    def All(self):
        return self.__All
    @property
    def nodes(self):
        return self.__nodes
    @property
    def parentNode(self):
        return self.__parentNode
    @parentNode.setter
    def parentNode(self,value):
        self.__parentNode=value
    @property
    def wall(self):
        return self.__wall
    @wall.setter
    def wall(self,value1):
        self.__wall=value1
    def on_press(self):
        if self.text=='make wall':
            self.mkWall=True
        elif self.text== 'start':
            self.mkWall=False
            
        self.control()
        a=0
        
        
        # while a<20:
        #     v=randrange(600)
        #     v1=self.nodes[v]
        #     self.nodes.remove(v1)
        #     v1.background_color=[0,0,0,1]
        #     a+=1
        # print(self.pos)
        
        # self.background_color=[1,0,0,1]        
    def neighbors(self):
        point=self.pos
        neighbors=[]
        
        for i in [-20,20]:
            x,y=point[0]+i,point[1]+i
            if x in range(48*20):
                n1=self.__All[f'[{x},{point[1]}]']
                if n1 in self.__nodes:
                    neighbors.append(n1)
                    n1.parentNode=self
                    self.__nodes.remove(n1)
            if y in range(30*20):
                n2=self.__All[f'[{point[0]},{y}]']
                if n2 in self.__nodes:
                    neighbors.append(n2)
                    n2.parentNode=self
                    self.__nodes.remove(n2)
        return neighbors   
    def draw_path(self):
        t=1
        self.background_color=[0,0,1,1]
        next_node=self.parentNode
        self.text="n"
        path=[]
        while next_node!=Stor.head[0]:
            path.append(next_node)
            next_node=next_node.parentNode
            
        for i in path[::-1]:
            sleep(.1)
            i.background_color=[0,0,1,.75]
            # i.text=f'{t}'
            t+=1
    def wall_block(self,const,big,small,s=0):
        if s==0:
            for i in range(small,big+20,20):
                a=self.__All[f'[{const},{i}]']
                if a in self.__nodes:
                    self.nodes.remove(a)
                    a.background_color=[0,0,0,1]
        else:
            for i in range(small,big+20,20):
                a=self.__All[f'[{i},{const}]']
                if a in self.nodes:
                    self.nodes.remove(a)
                    a.background_color=[0,0,0,1]       
    def create_Wall(self):
        
        if self.__All[f"[{self.pos[0]},{self.pos[1]}]"] in self.__nodes:
            
            if  self.wallHead==None:
                self.wallHead=self
                self.background_color=[1,0,0,1]  
            else:
                x,y=self.wallHead.pos[0],self.wallHead.pos[1]
                sx,sy=self.pos[0],self.pos[1]
                if x==sx:
                    if sy/y>1:
                        self.wall_block(x,sy,y)
                    elif sy/y<1:
                        self.wall_block(x,y,sy)
                elif y==sy:
                    if sx/x>1:
                        self.wall_block(y,sx,x,s=1)
                    elif sx/x<1:
                        self.wall_block(y,x,sx,s=1)
                self.wallHead=None                          
    def control(self):
        if self.mkWall:
            self.create_Wall()
        else:
            if self.text!='start':
                if len(Stor.head)==0:
                    Stor.stor_head(self)
                    self.background_color=[0,1,.45,1]
                else:
                    Stor.stor_target(self)
                    s=BFS(self)
                    
                    tr=threading.Thread(target=s.search,args=(Stor.head[0],)).start()
                    tr           
    def reset(self):
        for i in self.__All:
            self.__All[i].text=" "
            self.__All[i].background_color=[1,1,1,.9]
            Stor.head.clear()
            Stor.target.clear()           
    def __repr__(self) -> str:
        return f'[{self.pos[0]},{self.pos[1]}]'
        
class Main(App):
    def build(self):
        return Window()
    
if __name__=='__main__':
    Main().run()
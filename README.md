# iGrab  
我去图书馆抢座助手python实现 V1.0  
前言：github上已经有我去图书馆抢座助手的python实现，但实现的过于复杂，而且已经缺乏维护。  
正好我有兴趣写一写图书馆抢座程序，请大家批评  
  
**已实现的功能**  
  
*快速抢座*  
不断刷新图书馆座位，有余座就帮你抢上  
  
*特定楼层抢座*  
只抢特定楼层的座位。该功能不具有普适性，待完善  
  
**项目文件介绍**  
  
*cookie_loop.py*:读取cookie文件，每隔五分钟向服务器发送请求并实现cookie文件的更新  
*cookie.json*:存放昵称和相应的cookie文件  
*reserve_quickly.py*:快速抢座，运行后输入昵称便可抢座  
*reserve_specific_floor.py*:抢特定楼层的座位。注意，我在文件中写的代号对其他学校不起作用，此文件可忽略，或者你自己改一下  
  
**使用方法**  
  
先抓包，用自己的cookie添加到cookie.json的cookie中（昵称随意），然后开始运行cookie_loop.py。之后即可运行reserve_quickly.py进行抢座  
ps:我的程序是跑在服务器上的，如果你跑在自己的电脑上，关机或关闭cookie_loop.py程序会使cookie无法保持最新，那你可能每次都要先手动抓包，添加到cookie.json上然后再运行reserve_quickly.py  
  
**下一步计划**
  
1.定时抢座  
2.明日预约

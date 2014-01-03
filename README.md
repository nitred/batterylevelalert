batterylevelalert
=================

Laptop Batteries and any batteries for that matter have a range of optimum charge levels, within which the battery life is prolonged. The script alerts the user to connect / disconnect the charger when the charge goes above or below the optimum charge range.

I've read somewhere that maintaining the battery levels of Lithium Ion Batteries between 40% to 80% would be optimum and improve battery life as well. I'm unable to find the link currently but here are a few other similar sources.

Link 1 : http://batteryuniversity.com/learn/article/how_to_prolong_lithium_based_batteries

Link 2 : http://zeusbatteryproducts.wordpress.com/2012/08/22/5-best-storage-and-charging-tips-for-extending-lifespan-of-lithium-ion-batteries-in-home-business/

03-01-2014 (DD-MM-YYYY)

So,
I'm currently testing on a DELL STUDIO LAPTOP running Windows 7

I've written a script for myself in Python 2.7.6 and converted it into a Windows .exe file using Py2exe which is very easy to do.

If you're on Linux you can just remove the timer part of the script and use a cron job to run it every minute(so I've heard).

I have no experience with Macs
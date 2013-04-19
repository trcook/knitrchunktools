import sublime
import sublime_plugin
import os
import subprocess
import string
import re
import Rtools

class SendChunkCommand(sublime_plugin.TextCommand):
  def run(self, view): # runs on command
    mysel=self.view.find_all('(?<=>>=\n)((.*\n)+?)(?=@)')
    cur_chunk = []
    init_sel = int(self.view.sel()[0].a) # sets initial selection position - need to pull it out this way to prevent updating later. It also makes setting the cursor position later a little easier
    print init_sel.__class__, init_sel
    for sel in mysel:
        if sel.a<= self.view.sel()[0].a <=sel.b:
            # following two lines help with debugging
            #print sel.a, sel.b
            #print sel.__class__
            cur_chunk.append(sublime.Region(sel.a+1,sel.b-1))
      #  else:
          #  print "not", sel.a, sel.b

    # print "cur chunk is", cur_chunk
    # to capture the chunk as a string: 
    # self.view.substr(cur_chunk[0])
    # print self.view.sel()[0].begin() 

    # the self.view.sel() method returns, essentially a nested list (called an object of class RegionSet -- which is  a collection of regions). So the part that is [0] indexes the first region in the region set (which is, of course, the only region in the region set), and the '.begin()' call gets the starting point for the region.
    
    # print self.view.sel()[0].a # this line does the same, but uses the (for our purposes here) synonymous term 'a'

    

    # print cur_chunk.__class__
    # print cur_chunk[0].a
    
    self.view.sel().add(cur_chunk[0])
    # print self.view.scope_name(self.view.sel()[0].b)
    self.view.run_command('send_selection') # this runs the send_selection command from r-tools. I have yet to figure out how to work this so that it runs w/o manually setting the syntax to r (i.e. there is some scope issues at play)
    print init_sel.__class__, init_sel
    self.view.sel().subtract(cur_chunk[0])
    self.view.sel().add(sublime.Region(init_sel))
    #self.view.show(init_sel[0].a)
    return 


class NextChunkCommand(sublime_plugin.TextCommand):
    def run(self,edit):
        init_sel = int(self.view.sel()[0].a)
        mysel=self.view.find_all('(?<=>>=\n)((.*\n)+?)(?=@)')
        cur_chunk = []
        chunk_number = []
        print range(0,len(mysel),1)
        for sel in range(0,len(mysel),1):
            if mysel[sel].b> self.view.sel()[0].a<mysel[sel].a:
                cur_chunk.append(mysel[sel])
                chunk_number.append(sel)
                break

        if cur_chunk != []:
            self.view.show(cur_chunk[0].a)
            self.view.sel().clear()
            self.view.sel().add(sublime.Region(cur_chunk[0].a))
            print "there are ", len(mysel),"chunks, you are at chunk:" ,chunk_number[0]
        else:
            print "there are ", len(mysel),"chunks, you are at chunk:" ,len(mysel)
            print "end of file reached with no more chunks"

        return

class PrevChunkCommand(sublime_plugin.TextCommand):
    def run(self,edit):
        init_sel = int(self.view.sel()[0].a)
        mysel=self.view.find_all('(?<=>>=\n)((.*\n)+?)(?=@)')
        cur_chunk = []
        chunk_number = []
        print range(len(mysel)-1,-1,-1)
        for sel in range(len(mysel)-1,-1,-1):
            if mysel[sel].b< self.view.sel()[0].a>mysel[sel].a:
                cur_chunk.append(mysel[sel])
                chunk_number.append(sel)
                break
                
        if cur_chunk != []:
            self.view.show(cur_chunk[0].a)
            self.view.sel().clear()
            self.view.sel().add(sublime.Region(cur_chunk[0].a))
            print "there are ", len(mysel),"chunks, you are at chunk:" ,chunk_number[0]
        else:
            print "there are ", len(mysel),"chunks, you are at chunk:" , 1
            print "start of file reached with no more chunks"

        return
# setup a menu to choose which chunk to send. 
# maybe use a for loop for this: 
# for each match, in the number of matches, set selection to the match if  the cursor is between the minimum of that match and the maximum of that match. You should be able to set this condition by mysel[b].a<=cursor<=max(x[2]) where x is the region of the match and cursor is whatever code is needed to get the cursor position 
 

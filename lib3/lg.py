# Basic config for logging module to use
import os
import sys 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
import time
from logging import *
from logging.handlers import *

# configs
log_file_name = "test.log"
log_level = DEBUG
from config.base import App, Env, Configured, ENV_PRODUCTION
if len(App) > 0 and len(Env) > 0 and Configured:
    log_file_name = App+"_"+Env+".log"
    if Env == ENV_PRODUCTION:
        log_level = INFO

print(log_file_name)
# https://docs.python.org/2/library/logging.handlers.html#timedrotatingfilehandler
when = "midnight"
intval = 1
maxbytes = 1024*1024*1024
backcount = 1000

class EnhancedRotatingFileHandler(TimedRotatingFileHandler):
    def __init__(self, filename, when='h', interval=1, backupCount=0, encoding=None, delay=0, utc=0, maxBytes=0):
        """ This is just a combination of TimedRotatingFileHandler and RotatingFileHandler (adds maxBytes to TimedRotatingFileHandler)  """
        TimedRotatingFileHandler.__init__(self, filename, when, interval, backupCount, encoding, delay, utc)
        self.maxBytes=maxBytes

    def shouldRollover(self, record):
        """
        Determine if rollover should occur.

        Basically, see if the supplied record would cause the file to exceed
        the size limit we have.

        we are also comparing times
        """
        if self.stream is None:                 # delay was set...
            self.stream = self._open()
        if self.maxBytes > 0:                   # are we rolling over?
            msg = "%s\n" % self.format(record)
            self.stream.seek(0, 2)  #due to non-posix-compliant Windows feature
            if self.stream.tell() + len(msg) >= self.maxBytes:
                return 1
        t = int(time.time())
        if t >= self.rolloverAt:
            return 1
        #print "No need to rollover: %d, %d" % (t, self.rolloverAt)
        return 0

    def doRollover(self):
        """
        do a rollover; in this case, a date/time stamp is appended to the filename
        when the rollover happens.  However, you want the file to be named for the
        start of the interval, not the current time.  If there is a backup count,
        then we have to get a list of matching filenames, sort them and remove
        the one with the oldest suffix.
        """
        if self.stream:
            self.stream.close()
        # get the time that this sequence started at and make it a TimeTuple
        currentTime = int(time.time())
        dstNow = time.localtime(currentTime)[-1]
        t = self.rolloverAt - self.interval
        if self.utc:
            timeTuple = time.gmtime(t)
        else:
            timeTuple = time.localtime(t)
            dstThen = timeTuple[-1]
            if dstNow != dstThen:
                if dstNow:
                    addend = 3600
                else:
                    addend = -3600
                timeTuple = time.localtime(t + addend)
        dfn = self.baseFilename + "." + time.strftime(self.suffix, timeTuple)
        if self.backupCount > 0:
            cnt=1
            dfn2="%s.%03d"%(dfn,cnt)
            while os.path.exists(dfn2):
                dfn2="%s.%03d"%(dfn,cnt)
                cnt+=1
            os.rename(self.baseFilename, dfn2)
            for s in self.getFilesToDelete():
                os.remove(s)
        else:
            if os.path.exists(dfn):
                os.remove(dfn)
            os.rename(self.baseFilename, dfn)
        #print "%s -> %s" % (self.baseFilename, dfn)
        self.mode = 'w'
        self.stream = self._open()
        newRolloverAt = self.computeRollover(currentTime)
        while newRolloverAt <= currentTime:
            newRolloverAt = newRolloverAt + self.interval
        #If DST changes and midnight or weekly rollover, adjust for this.
        if (self.when == 'midnight' or self.when.startswith('W')) and not self.utc:
            dstAtRollover = time.localtime(newRolloverAt)[-1]
            if dstNow != dstAtRollover:
                if not dstNow:  # DST kicks in before next rollover, so we need to deduct an hour
                    addend = -3600
                else:           # DST bows out before next rollover, so we need to add an hour
                    addend = 3600
                newRolloverAt += addend
        self.rolloverAt = newRolloverAt

    def getFilesToDelete(self):
        """
        Determine the files to delete when rolling over.

        More specific than the earlier method, which just used glob.glob().
        """
        dirName, baseName = os.path.split(self.baseFilename)
        fileNames = os.listdir(dirName)
        result = []
        prefix = baseName + "."
        plen = len(prefix)
        for fileName in fileNames:
            if fileName[:plen] == prefix:
                suffix = fileName[plen:-4]
                if self.extMatch.match(suffix):
                    result.append(os.path.join(dirName, fileName))
        result.sort()
        if len(result) < self.backupCount:
            result = []
        else:
            result = result[:len(result) - self.backupCount]
        return result

# NOTE: configure log file based on day, size 1G.
thandler = EnhancedRotatingFileHandler(log_file_name, when=when, interval=intval, backupCount=backcount, maxBytes=maxbytes)
thandler.suffix = "%Y-%m-%d_%H:%M:%S"

def ConfigLogger(logger):
    logger.addHandler(thandler)

#basicConfig(filename=log_file_name, level=log_level, format='%(asctime)s: %(levelname)s: %(filename)s:%(lineno)d: %(funcName)s: %(message)s', handlers=[thandler])
basicConfig(level=log_level, format='%(asctime)s: %(levelname)s: %(filename)s:%(lineno)d: %(funcName)s: %(message)s', handlers=[thandler])
logger = getLogger(log_file_name)
# Using any handler may result in undesired behavior(lost basic config like filename,funcname, etc)
#ConfigLogger(logger)

def main():
    logger.info("ok")

if __name__ == '__main__':
    main()

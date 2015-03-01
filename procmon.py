import psutil, time, sys, signal
from datetime import datetime
from optparse import OptionParser

def main():
  # Setup command-line arugments
  parser = OptionParser()
  parser.add_option('-o', '--output', action='store', dest='filename', default='output.csv', help='Output file name/location. Default is output.csv', metavar='OUTPUT')
  parser.add_option('-p', '--process-name', action='store', dest='procname', help='Process name', metavar='PROCESS')
  parser.add_option('-t', '--title', action='store', dest='title', default='FALSE', help='Specifies whether to include a title row', metavar='BOOLEAN')
  (options, args) = parser.parse_args()

  # Check if there is a process name argument
  if options.procname is None:
    print 'No process name. Use -p to specifiy a process name.'
    sys.exit()

  # Setup vars
  procname = options.procname
  filename = options.filename

  # Create file and write header line
  f = open(filename, 'w')
  if options.title == 'TRUE':
    f.write('Time, RAM, CPU\n')

  # Handle ctrl-c interrupt, close file gracefully
  def signal_handler(signal, frame):
    print '\nExiting. Output in ' + filename
    f.close()
    sys.exit(0)
  signal.signal(signal.SIGINT, signal_handler)

  # Repeat forever, iterate by 1s
  while True:
    totalmem = 0
    totalcpu = 0
    timestamp = datetime.now().strftime('%H:%M:%S')

    # Iterate through all processes, search for process name in arg
    # and total RAM and CPU usage for all process with that name.
    # Then write to file with a csv format
    for proc in psutil.process_iter():
      if proc.name() == procname:
        totalmem = totalmem + proc.memory_percent()
        totalcpu = totalcpu + proc.cpu_percent(interval = None)

    f.write(timestamp + ',' + repr(totalmem) + ',' + repr(totalcpu) +'\n')
    time.sleep(1)

if __name__ == '__main__':
  main()

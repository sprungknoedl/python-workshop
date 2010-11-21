import sys; map(sys.stdout.write, (word + "\n" for line in sys.stdin for word in line.split() if '@' in word))

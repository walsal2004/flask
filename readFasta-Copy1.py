def readFasta(filename1):
    sequences = []
    
    with open(filename1) as fh:
        while True:
            fh.readline()
            seq = fh.readline().rstrip()
            fh.readline()
            if len(seq) == 0:
                break
            sequences.append(seq)
            
    return sequences
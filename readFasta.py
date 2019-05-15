def readFasta(filename1):
    sequences = []
    count = 0
    lines = filename1.split('\n')
    for line in lines:
        count+=1
        if count % 2 == 0:
            seq = line   
            sequences.append(seq)
        
            
    return sequences
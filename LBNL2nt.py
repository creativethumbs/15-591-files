import string

inputFile1 = open('LBNL-sdp.dat', 'r')
#inputFile2 = open('allNodes.csv', 'r')
outputFile = open('LBNL.nt', 'w')

def makeOutput():
    for line in inputFile1:
        record = string.split(line, "\t")
        srcip = record[0].rstrip()
        dstip = record[1].rstrip()
        port = record[2].rstrip()

        outputFile.write("<http://ip/" + srcip + ">" + 
            " <http://has_dest> <http://ip/" + dstip + "> .\n") 

        outputFile.write("<http://ip/" + srcip + ">" + 
            " <http://on_port> <http://port/" + port + "> .\n") 

        #vector table
        outputFile.write("<http://ip/" + srcip + ">" + 
            " <http://vector-a-score1> \"0.001\" .\n") 

        outputFile.write("<http://ip/" + dstip + ">" + 
            " <http://vector-b-score1> \"0.001\" .\n") 

        outputFile.write("<http://port/" + port + ">" + 
            " <http://vector-c-score1> \"0.001\" .\n") 
         

makeOutput()

inputFile1.close()  
outputFile.close() 

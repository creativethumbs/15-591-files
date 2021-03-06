import string

inputFile1 = open('edgefile.txt', 'r')
inputFile2 = open('allNodes.csv', 'r')
outputFile = open('eigen.nt', 'w')

def makeOutput():
    for line in inputFile1:
        record = string.split(line, " ")
        src = record[0].rstrip()
        dst = record[1].rstrip()

        outputFile.write("<http://vert/" + src + ">" + 
            " <http://link> <http://vert/" + dst + "> .\n") 
        
    for line in inputFile2:
        src = line.rstrip() 

        outputFile.write("<http://vert/" + src + ">" + 
            " <http://scoreiter1> \"0.001\" .\n") 

makeOutput()

inputFile1.close() 
inputFile2.close()
outputFile.close() 

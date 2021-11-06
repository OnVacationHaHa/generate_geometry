import os
from os import listdir


def GetNodesGeom(fileStr):
    dic4nodes = dict()
    files = listdir(fileStr)
    for f in files:
        if "node" in f:
            with open(fileStr + "/" + f, 'r') as F:
                line = F.readline()
                line = line.replace('\n', '').replace('\r', '')
                cells = line.split(',')
                idIndex = cells.index("node_id")
                xIndex = cells.index("x_coord")
                yIndex = cells.index("y_coord")
                lines = F.readlines()
                for line in lines:
                    cells = line.split(',')
                    nodeID = int(cells[idIndex])
                    xCoord = float(cells[xIndex])
                    yCoord = float(cells[yIndex])
                    dic4nodes[nodeID] = (xCoord, yCoord)
            return dic4nodes
    return None


def GenerateLinkWithGeom(fileStr, outputStr, dic4nodes):
    files = listdir(fileStr)
    for f in files:
        if "link" in f:
            with open(fileStr + "/" + f, 'r') as F:
                with open(outputStr + "/link.csv", 'w+') as F2:
                    line = F.readline().replace('\r','').replace('\n','')
                    cells = line.split(',')
                    F2.write(line + ',geometry')
                    F2.write('\n')
                    fromIndex = cells.index("from_node_id")
                    toIndex = cells.index("to_node_id")
                    lines = F.readlines()
                    for line in lines:
                        line=line.replace('\r','').replace('\n','')
                        cells = line.split(',')
                        fromID = int(cells[fromIndex])
                        toID = int(cells[toIndex])
                        F2.write(line)
                        if fromID in dic4nodes and toID in dic4nodes:
                            fromGeom = dic4nodes[fromID]
                            toGeom = dic4nodes[toID]
                            geom = '"LINESTRING ({0} {1}, {2} {3})"'.format(fromGeom[0], fromGeom[1], toGeom[0],
                                                                            toGeom[1])
                            F2.write("," + geom)
                        F2.write('\n')


if __name__ == "__main__":
    if not os.path.exists('./input'):
        print("Please create an ‘input’ folder in '{0}' directory and put the input files in this folder".format(os.getcwd()))
    else:
        dic4nodes = GetNodesGeom('./input')
        if dic4nodes is not None:
            files = listdir('./input')
            anyLink=False
            for f in files:
                if 'link' in f:
                    anyLink=True
                    break
            if not anyLink:
                print('no link file')
            else:
                if not os.path.exists('./output'):
                    os.makedirs('./output')
                del_list = os.listdir('./output')
                for f in del_list:
                    file_path = os.path.join('./output', f)
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                    elif os.path.isdir(file_path):
                        import shutil
                        shutil.rmtree(file_path)
                GenerateLinkWithGeom('./input', './output', dic4nodes)
                print("OK")
        else:
            print("'node' file is wrong ")

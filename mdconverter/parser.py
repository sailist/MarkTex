import re
from .containers import markCode



def findBound(pattern, lines, start_index,expand = False):
    end_index = start_index
    max_line = len(lines)
    while True:
        if end_index + 1 == max_line:
            return start_index, end_index
        if (expand and len(lines[end_index+1]) > 0 ) or re.search(pattern, lines[end_index + 1]):
            end_index += 1
        else:
            return start_index, end_index

def findCodeBound(lines,start_index):
    end_index = start_index
    line_num = len(lines)
    codeTemplate = re.search(markCode,lines[start_index]).group(1)
    while end_index+1<line_num:
        # print(lines[end_index+1])
        if re.search(markCode,lines[end_index+1]):
            return codeTemplate,start_index,end_index
        else:
            pass
            # print(lines[end_index+1])
        end_index+=1

    # return codeTemplate,start_index,end_index
    assert end_index+1 < line_num


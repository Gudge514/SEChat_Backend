import logging
logger = logging.getLogger(__name__)

def parseDocument(con):
    
    import re
    import json
    
    headings = []
    current_heading = None

    for line in con:
        line = line.strip()
        if re.match(r'^\d+(\.\d+)*\s+', line):
            if current_heading:
                headings.append(current_heading)
            level, title = re.split(r'\s+', line, maxsplit=1)
            current_heading = {
                'level': level,
                'title': title,
                'content': ""
            }
        else:
            if current_heading:
                current_heading['content']+=line+"\n"

    if current_heading:
        headings.append(current_heading)

    l = len(headings)
    for i in range(l):
        for j in range(i):
            if headings[i-j-1]["level"].split(".") == headings[i]["level"].split(".")[0:len(headings[i]["level"].split("."))-1]:
                headings[i]["title"] = headings[i-j-1]["title"] + " " + headings[i]["title"]

    headings = [heading for heading in headings if heading["content"]!=""]
    logger.info("文本已解析")
    return headings


# 解析json
def parseJson(answer):
    import json
    
    left = answer.index("{")
    right = answer.index("{")
    output = []
    cnt = 1
    
    while(left<len(answer) and right<len(answer)):
        right+=1
        if right>=len(answer):
            logger.info(answer)
            return output
        if answer[right] == "}":
            cnt-=1
        if answer[right] == "{":
            cnt+=1
        if cnt==0:
            try:
                answer_json = json.loads(answer[left:right+1].replace("\n", "").replace("  ", "").replace("，",",").replace("。",".").replace("\\","").replace(",}","}").replace("'",'"'))    
                if len(answer_json.keys())==1:
                    answer_json = answer_json[list(answer_json.keys())[0]]
                output.append(answer_json)
            except:
                # print(f"error from:{left} to {right}")
                # print(answer[left:right+1])
                # print()
                
                logger.error(f"error from:{left} to {right}")
                logger.error(answer[left:right+1])
                
            left = right+1
            while(left<len(answer) and answer[left]!="{"):
                left+=1
            right = left
            cnt = 1
    if len(output)==1:
        return output[0]
    return output
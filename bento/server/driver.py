"""
Executed in environment generated by server
"""

import json
import base64
import sys
import logging
import core.bentoapi as bentoapi


def __execute(code, call):
    """
    Load the function's context and then execute it
    """
    context = dict(locals(), **globals())
    context['api']= bentoapi
    byte_code= compile(code, '<inline>', 'exec')
    exec(byte_code, context, context)
    return eval(call, context) 

    

def __main():
    """
    Parse function code and call from argument and execute
    """
    todo= sys.argv[1]

    exec_data= json.loads(base64.urlsafe_b64decode(todo.encode()).decode())
    
    call= exec_data['call']
    code= exec_data['code']

    # execute the function and send any return value back
    retval= __execute(code, call)
    data=str(retval)#干脆将全部输出都转化为string类型的数据
    bentoapi.send(data) 


__main()
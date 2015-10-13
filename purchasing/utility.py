# coding: UTF-8
from datetime import datetime
from purchasing.models import StatusChange

def goNextStatus(bidform,user):
    original_status=bidform.bid_status
    new_status=original_status.next_part_status
    change_time=datetime.now()
    status_change=StatusChange(bidform=bidform,original_status=original_status,new_status=new_status,change_user=user,change_time=change_time)
    status_change.save()
    bidform.bid_status=new_status
    bidform.save()

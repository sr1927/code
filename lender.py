import json


class Lender:
    def __init__(self, lender_id,name,image_id,template_id,whereabouts,country_code,uid,member_since,personal_url,occupation,loan_because,
        occupational_info,loan_count,invitee_count,inviter_id):
        self.lender_id = lender_id
        self.name = name
        self.image_id = image_id
        self.template_id = template_id
        self.whereabouts = whereabouts
        self.country_code = country_code
        self.uid = uid
        self.member_since = member_since
        self.personal_url = personal_url
        self.occupation = occupation
        self.loan_because = loan_because
        self.occupational_info = occupational_info
        self.loan_count = loan_count
        self.invitee_count = invitee_count
        self.inviter_id = inviter_id        
        
    def toJson(self):
        return json.dumps(self.__dict__, cls=SetEncoder)

class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder(self, obj)


def fromJson(json_string):
    json_map = json.loads(json_string)
    return Lender(json_map["lender_id"], json_map["name"], json_map["image_id"], json_map["template_id"],
                json_map["whereabouts"], json_map["country_code"],json_map["uid"] ,json_map["member_since"] ,
                json_map["personal_url"] ,json_map["occupation"] ,json_map["loan_because"],json_map["occupational_info"],
                json_map["loan_count"],json_map["invitee_count"],json_map["inviter_id"])


def __str__(self):
    return  self.lender_id+":"+self.name+":"+self.image_id+":"+self.template_id +":"+self.whereabouts +":"+self.country_code +":"+self.uid 
    +":"+self.member_since+":"+self.personal_url +":"+self.occupation +":"+self.loan_because+ self.occupational_info+self.loan_count+ self.invitee_count+self.inviter_id   

def __unicode__(self):
        return  self.lender_id+":"+self.name+":"+self.image_id+":"+self.template_id +":"+self.whereabouts +":"+self.country_code +":"+self.uid 
        +":"+self.member_since+":"+self.personal_url +":"+self.occupation +":"+self.loan_because+ self.occupational_info+self.loan_count+ self.invitee_count+self.inviter_id   


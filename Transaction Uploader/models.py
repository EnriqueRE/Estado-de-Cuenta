__author__ = 'enriqueramirez'
import json
import urllib2, base64


class PreAccountStatement:
    def fix_date (self, date):
        dates = date.split('.')
        dates[0], dates[-1] = dates[-1], dates[0]
        return '-'.join(dates)

    def to_json (self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def __init__ (self, line):
        self.statement_date = self.fix_date(line[8])
        self.statement_student = line[3]
        self.statement_value = line[13]
        self.statement_code = line[4]

    def __unicode__ (self):
        return "{%s, %s, %s, %s}" % (
            self.statement_date, self.statement_student, self.statement_code,
            self.statement_value)


class AccountStatement:
    def __init__ (self, student_id, date, tuition, interests, positive,
                  insurance,
                  services):
        self.statement_student = student_id
        self.statement_date = date
        self.statement_tuition = tuition
        self.statement_interests = interests
        self.statement_positive_balance = positive
        self.statement_insurance = insurance
        self.statement_diverse_services = services

    def to_json (self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def upload_to_server (self):
        request = urllib2.Request(
            "http://riego.chi.itesm.mx:8080/Statement/")
        request.add_header("Authorization", "Basic YWRtaW46YWRtaW4=")
        request.add_header("Content-Type", "application/json")
        request.get_method = lambda: 'POST'
        print self.to_json()
        result = urllib2.urlopen(request, self.to_json())


class MonederoUser:
    def __init__ (self,row):
        self.student_id = row[0]
        self.student_name = row[2]
        self.student_lastname = row[3]
        self.student_second_lastname = row[4]
        self.student_badge_id = row[5]
        self.student_email = self.student_id + "@itesm.mx"

    def to_json (self):
        return json.dumps(self, default=lambda direct: direct.__dict__,
                          sort_keys=True, indent=4)

    def upload_to_server (self):
        request = urllib2.Request(
            "http://riego.chi.itesm.mx:8080/User/")
        request.add_header("Authorization", "Basic YWRtaW46YWRtaW4=")
        request.add_header("Content-Type", "application/json")
        request.get_method = lambda: 'POST'
        print self.to_json()
        result = urllib2.urlopen(request, self.to_json())

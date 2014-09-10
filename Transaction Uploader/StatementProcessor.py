__author__ = 'admin'

import urllib2, base64
from models import AccountStatement

CHARGES_DICTIONARY = {
    # Colegiatura
    '3010': 'Tuition',
    '5510': 'Tuition',
    '5520': 'Tuition',
    '5550': 'Tuition',
    '8010': 'Tuition',
    '9010': 'Tuition',
    '9020': 'Tuition',
    '9050': 'Tuition',
    '9101': 'Tuition',
    '9107': 'Tuition',
    '9180': 'Tuition',
    '9190': 'Tuition',
    '9801': 'Tuition',
    '9802': 'Tuition',
    # Intereses Comisiones y penalidades
    '40': 'icp',
    '681': 'icp',
    '682': 'icp',
    '683': 'icp',
    '9103': 'icp',
    '9109': 'icp',
    '9110': 'icp',
    '9120': 'icp',
    '9150': 'icp',
    '9210': 'icp',
    '9220': 'icp',
    '9250': 'icp',
    '9410': 'icp',
    '9420': 'icp',
    '9450': 'icp',
    # Saldo a favor
    '50': 'saldo',
    '500': 'saldo',
    # Seguros
    '9000': 'seguros',
    '9111': 'seguros',
    # Servicios diversos
    '661': 'servicios',
    '1607': 'servicios',
    '1613': 'servicios'
}


class StatementProcessor:
    @staticmethod
    def search_for_statements_by_student (list, student_id):
        matches = [x for x in list if x.statement_student == student_id]
        return matches

    @staticmethod
    def process_transactions(statements, student):
        tmp_services = 0.0
        tmp_insurance = 0.0
        tmp_credit = 0.0
        tmp_interests = 0.0
        tmp_tuition = 0.0
        for statement in statements:
            # Checking for tuition
            if statement.statement_code == '3010' \
                    or statement.statement_code == '5510' \
                    or statement.statement_code == '5520' \
                    or statement.statement_code == '5550' \
                    or statement.statement_code == '8010' \
                    or statement.statement_code == '9010' \
                    or statement.statement_code == '9020' \
                    or statement.statement_code == '9050' \
                    or statement.statement_code == '9101' \
                    or statement.statement_code == '9107' \
                    or statement.statement_code == '9180' \
                    or statement.statement_code == '9190' \
                    or statement.statement_code == '9801' \
                    or statement.statement_code == '9802':

                tmp_tuition += float(statement.statement_value)
            # Checking for ICP's
            elif statement.statement_code == '3010' \
                    or statement.statement_code == '40' \
                    or statement.statement_code == '681' \
                    or statement.statement_code == '682' \
                    or statement.statement_code == '683' \
                    or statement.statement_code == '9103' \
                    or statement.statement_code == '9109' \
                    or statement.statement_code == '9110' \
                    or statement.statement_code == '9120' \
                    or statement.statement_code == '9150' \
                    or statement.statement_code == '9210' \
                    or statement.statement_code == '9220' \
                    or statement.statement_code == '9250' \
                    or statement.statement_code == '9410' \
                    or statement.statement_code == '9420' \
                    or statement.statement_code == '9450':
                tmp_interests += float(statement.statement_value)
            # Checking for credit
            elif statement.statement_code == '50' or statement.statement_code == '500':
                tmp_credit += float(statement.statement_value)
            # Checking for Insurance
            elif statement.statement_code == '9000' or statement.statement_code == '9111':
                tmp_insurance += float(statement.statement_value)
                # Checking for services
            elif statement.statement_code == '661' \
                    or statement.statement_code == '1607' \
                    or statement.statement_code == '1613':
                tmp_services += float(statement.statement_value)

        account_statement = AccountStatement(student,
                                             statement.statement_date,
                                             abs(tmp_tuition),
                                             abs(tmp_interests),
                                             abs(tmp_credit),
                                             abs(tmp_insurance),
                                             abs(tmp_services))

        #print account_statement.to_json()
        account_statement.upload()
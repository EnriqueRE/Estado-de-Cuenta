import user

__author__ = 'Enrique Ramirez'
from StringIO import StringIO
import ldap, ldif, ldap.sasl, sys

RESPONSE_DICTIONARY = {1: 'Valid user', 2: 'Invalid user', 3: 'Wrong Credentials', 4: 'Server is Down'}


def search_for_user(user):
    """Searches the LDAP Server for user email on server
       :param user: user's email
       :return user ldap's dn

    """
    try:
        ld = ldap.initialize('ldap://10.32.70.13:389')
        ld.simple_bind_s()
        basedn = ""
        filter = "(&(mail=" + user + "))"
        results = ld.search_s(basedn, ldap.SCOPE_SUBTREE, filter)
        tmpString = StringIO()
        ldifWriter = ldif.LDIFWriter(tmpString)

        result = ""

        for dn, entry in results:
            ldifWriter.unparse(dn, entry)
            result = dn
        return result

    except ldap.SERVER_DOWN:
        return ""


def authenticate_user(user_email, user, password):
    """ Authenticates user on LDAP server.
    :param user_email: user's email.
    :param user:
    :param password:
    :return: List with message and code
    """

    query_result = []

    try:
        # build a client
        ldap_client = ldap.initialize('ldap://10.32.70.13:389')
        # perform a synchronous bind
        # ldap_client.set_option(ldap.OPT_REFERRALS, 0)
        ldap_client.simple_bind_s(user, password)

    except ldap.INVALID_CREDENTIALS:
        ldap_client.unbind()
        query_result.append(3)
        query_result.append(RESPONSE_DICTIONARY.get(3))
        return query_result
    except ldap.SERVER_DOWN:
        query_result.append(4)
        query_result.append(RESPONSE_DICTIONARY.get(4))
        return query_result

    filter = "(&(mail=" + user_email + "))"
    results = ldap_client.search_s("", ldap.SCOPE_SUBTREE, filter)

    ldif_writer = ldif.LDIFWriter(sys.stdout)
    for dn, entry in results:
        print ldif_writer.unparse(dn, entry)

    query_result.append(1)
    query_result.append(RESPONSE_DICTIONARY.get(1))
    return query_result
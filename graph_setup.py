__author__ = "RAMichel"

import sys
import getopt
from rexpro import RexProConnection

# all of our builds for the titan graph
VERTEX_LABEL_BUILD = """
    mgmt = g.getManagementSystem()
    account = mgmt.makeVertexLabel('account').make()
    person = mgmt.makeVertexLabel('person').make()
    credit_card = mgmt.makeVertexLabel('credit_card').make()
    contact_info = mgmt.makeVertexLabel('contact_info').make()
    sale = mgmt.makeVertexLabel('sale').make()
    location = mgmt.makeVertexLabel('location').make()
    mgmt.commit()
    """

EDGE_LABEL_BUILD = """
    mgmt = g.getManagementSystem()
    cc_info = mgmt.makeEdgeLabel('cc_info').multiplicity(MULTI).make()
    contact = mgmt.makeEdgeLabel('contact').multiplicity(MULTI).make()
    located = mgmt.makeEdgeLabel('located').multiplicity(MULTI).make()
    purchased = mgmt.makeEdgeLabel('purchased').multiplicity(MULTI).make()
    user = mgmt.makeEdgeLabel('user').multiplicity(MULTI).make()
    mgmt.commit()
    """

PROPERTY_BUILD = """
    mgmt = g.getManagementSystem()
    first_name = mgmt.makePropertyKey('first_name').dataType(String.class).cardinality(Cardinality.SINGLE).make()
    last_name = mgmt.makePropertyKey('last_name').dataType(String.class).cardinality(Cardinality.SINGLE).make()
    full_name = mgmt.makePropertyKey('full_name').dataType(String.class).cardinality(Cardinality.SINGLE).make()
    phone_number = mgmt.makePropertyKey('phone_number').dataType(String.class).cardinality(Cardinality.SINGLE).make()
    email = mgmt.makePropertyKey('email').dataType(String.class).cardinality(Cardinality.SINGLE).make()
    cc_first_six = mgmt.makePropertyKey('cc_first_six').dataType(String.class).cardinality(Cardinality.SINGLE).make()
    cc_last_four = mgmt.makePropertyKey('cc_last_four').dataType(String.class).cardinality(Cardinality.SINGLE).make()
    zipcode = mgmt.makePropertyKey('zipcode').dataType(String.class).cardinality(Cardinality.SINGLE).make()
    address1 = mgmt.makePropertyKey('address1').dataType(String.class).cardinality(Cardinality.SINGLE).make()
    address2 = mgmt.makePropertyKey('address2').dataType(String.class).cardinality(Cardinality.SINGLE).make()
    city = mgmt.makePropertyKey('city').dataType(String.class).cardinality(Cardinality.SINGLE).make()
    country = mgmt.makePropertyKey('country').dataType(String.class).cardinality(Cardinality.SINGLE).make()
    mgmt.commit()
    """

ADD_VERTEXES = """
    def person1 = g.addVertexWithLabel('person')
    def person2 = g.addVertexWithLabel('person')
    def person3 = g.addVertexWithLabel('person')
    def person4 = g.addVertexWithLabel('person')
    ElementHelper.setProperties(person1, 'first_name', 'John', 'last_name', 'Doe', 'full_name', 'John A Doe')
    ElementHelper.setProperties(person2, 'first_name', 'Jane', 'last_name', 'Doe', 'full_name', 'Jane K Doe')
    ElementHelper.setProperties(person3, 'first_name', 'Seymore', 'last_name', 'Butts', 'full_name', 'Seymore J Butts')
    ElementHelper.setProperties(person4, 'first_name', 'Roger', 'last_name', 'Rabbit', 'full_name', 'Roger T Rabbit')
    g.commit()
    def contact_info1 = g.addVertexWithLabel('contact_info')
    def contact_info2 = g.addVertexWithLabel('contact_info')
    def contact_info3 = g.addVertexWithLabel('contact_info')
    def contact_info4 = g.addVertexWithLabel('contact_info')
    def contact_info5 = g.addVertexWithLabel('contact_info')
    ElementHelper.setProperties(contact_info1, 'phone_number', '(817) 584-1294', 'email', 'jdoe@test.com')
    ElementHelper.setProperties(contact_info2, 'phone_number', '838-174-4462', 'email', 'jane.doe@test.com')
    ElementHelper.setProperties(contact_info3, 'phone_number', '919.827.0192', 'email', 'c77more@test.com')
    ElementHelper.setProperties(contact_info4, 'phone_number', '7817818888', 'email', 'rrab01@test.com')
    ElementHelper.setProperties(contact_info5, 'phone_number', '+118888888888', 'email', 'another@test.com')
    g.commit()
    def credit_card1 = g.addVertexWithLabel('credit_card')
    def credit_card2 = g.addVertexWithLabel('credit_card')
    def credit_card3 = g.addVertexWithLabel('credit_card')
    def credit_card4 = g.addVertexWithLabel('credit_card')
    def credit_card5 = g.addVertexWithLabel('credit_card')
    def credit_card6 = g.addVertexWithLabel('credit_card')
    def credit_card7 = g.addVertexWithLabel('credit_card')
    ElementHelper.setProperties(credit_card1, 'cc_first_four', '0141', 'cc_last_six', '981221')
    ElementHelper.setProperties(credit_card2, 'cc_first_four', '2231', 'cc_last_six', '582916')
    ElementHelper.setProperties(credit_card3, 'cc_first_four', '7821', 'cc_last_six', '018475')
    ElementHelper.setProperties(credit_card4, 'cc_first_four', '0987', 'cc_last_six', '291887')
    ElementHelper.setProperties(credit_card5, 'cc_first_four', '2231', 'cc_last_six', '136853')
    ElementHelper.setProperties(credit_card6, 'cc_first_four', '1221', 'cc_last_six', '029847')
    ElementHelper.setProperties(credit_card7, 'cc_first_four', '0529', 'cc_last_six', '123097')
    g.commit()
    def location1 = g.addVertexWithLabel('location')
    def location2 = g.addVertexWithLabel('location')
    def location3 = g.addVertexWithLabel('location')
    def location4 = g.addVertexWithLabel('location')
    def location5 = g.addVertexWithLabel('location')
    ElementHelper.setProperties(location1, 'address1', '123 Fake Street', 'address2', '', 'zipcode', '98271', 'city', 'Whuddup', 'country', 'USA')
    ElementHelper.setProperties(location2, 'address1', '7717 77th Avenue', 'address2', 'Apt 7', 'zipcode', '27177', 'city', 'NYC', 'country', 'USA')
    ElementHelper.setProperties(location3, 'address1', '2240 Manitoba Pass', 'address2', '', 'zipcode', 'MA48G8', 'city', 'Toronto', 'country', 'CA')
    ElementHelper.setProperties(location4, 'address1', '98112 Bunk Avenue', 'address2', '#8', 'zipcode', '39444', 'city', 'Somewhere', 'country', 'NA')
    ElementHelper.setProperties(location5, 'address1', '912 McCullough Place', 'address2', '', 'zipcode', '98271', 'city', 'Another City', 'country', 'USA')
    g.commit()
    def sale1 = g.addVertexWithLabel('sale')
    def sale2 = g.addVertexWithLabel('sale')
    def sale3 = g.addVertexWithLabel('sale')
    def sale4 = g.addVertexWithLabel('sale')
    def sale5 = g.addVertexWithLabel('sale')
    def sale6 = g.addVertexWithLabel('sale')
    def sale7 = g.addVertexWithLabel('sale')
    def sale8 = g.addVertexWithLabel('sale')
    g.commit()

    person1.addEdge('contact', contact_info1)
    person2.addEdge('contact', contact_info2)
    person3.addEdge('contact', contact_info3)
    person4.addEdge('contact', contact_info4)
    person3.addEdge('contact', contact_info5)
    person1.addEdge('cc_info', credit_card1)
    person1.addEdge('cc_info', credit_card2)
    person2.addEdge('cc_info', credit_card3)
    person3.addEdge('cc_info', credit_card4)
    person4.addEdge('cc_info', credit_card5)
    person4.addEdge('cc_info', credit_card6)
    person4.addEdge('cc_info', credit_card7)
    g.commit()
    person1.addEdge('located', location1)
    person2.addEdge('located', location2)
    person3.addEdge('located', location3)
    person4.addEdge('located', location4)
    person4.addEdge('located', location5)
    credit_card1.addEdge('located', location1)
    credit_card2.addEdge('located', location1)
    credit_card3.addEdge('located', location2)
    credit_card4.addEdge('located', location3)
    credit_card5.addEdge('located', location4)
    credit_card6.addEdge('located', location5)
    credit_card7.addEdge('located', location5)
    g.commit()
    """

DESTROY_ACTION = """
    g.V.remove()
    g.shutdown()
    TitanCleanup.clear(g)
"""

ACTIONS = ['build', 'insert_all', 'destroy', 'test_query']

def show_usage():
    print "graph_setup.py -g <graph_name_in_rexster> -a <action>"
    print "<action> can be one of:"
    for word in ACTIONS:
        print "\t{0}".format((word))

def main(argv):
    print "This system is assuming that there is a Titan instance running a Cassandra backend on your Localhost."

    # See if a graph name has been passed in
    try:
        opts, args = getopt.getopt(argv,"g:a:",["graph=", "action="])
    except getopt.GetoptError:
        show_usage()

    graph_to_use = 'graph'
    action_to_do = 'none'

    for opt, arg in opts:
        if opt == '-h':
            show_usage()
        elif opt in ("-g", "--graph"):
            graph_to_use = arg
            if not graph_to_use:
                print 'Chosen graph was nil. Defaulting to "graph".'
                graph_to_use = 'graph'
        elif opt in ("-a", "--action"):
            action_to_do = arg
            if not action_to_do or action_to_do not in ACTIONS:
                print 'No valid action chosen. Exiting.'
                show_usage()
                sys.exit(2)


    # attempt initial rexpro connection
    print "Attempting RexPro connection to Rexster local server."
    try:
        conn = RexProConnection('localhost', 8184, graph_to_use)

        conn.test_connection()
    except:
        print 'Failure to connect to localhost. Make sure you have your titan and rexstar instances are running.'
        sys.exit(2)

    try:
        if action_to_do == 'none':
            print 'No action chosen. Exiting to prevent extra inserts or graph collissions.'
            sys.exit(2)
        elif action_to_do == 'build':
            with conn.transaction():
                print conn.execute(PROPERTY_BUILD)
                print conn.execute(VERTEX_LABEL_BUILD)
                print conn.execute(EDGE_LABEL_BUILD)
            print 'Building the specific Labels and Keys for the system.'
        elif action_to_do == 'insert_all':
            with conn.transaction():
                print conn.execute(ADD_VERTEXES)
        elif action_to_do == 'test_query':
            # get all people: g.query().has('label', 'person').vertices()
            print 'Testing a query to make sure things work properly.'
            with conn.transaction():
                print conn.execute('g.V().map')
        elif action_to_do == 'destroy':
            print "The system is attempting to shut down the graph and completely clear it. Please wait."
            with conn.transaction():
                conn.execute(DESTROY_ACTION)
            print "System has cleared the graph. Please restart your Titan instance in order to re-access the graph via RexPro."
    except Exception as e:
        print "Error occurred while attempting RexPro transactions."
        print str(e)
        sys.exit(2)

if __name__ == "__main__":
    main(sys.argv[1:])

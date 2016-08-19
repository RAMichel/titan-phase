__author__ = "RAMichel"

import sys
import getopt
from rexpro import RexProConnection

QUERY_ALL_PEOPLE = """
	def verts = g.query().has('label', 'person').vertices()
	return verts
	"""

ACTIONS = ['all_people', 'all_people_plus']

def show_usage():
    print "graph_setup.py -g <graph_name_in_rexster> -a <action>"
    print "<action> can be one of:"
    for word in ACTIONS:
        print "\t{0}".format((word))

def main(argv):
    print "This system is assuming that there is a Titan instance running a Cassandra backend on your Localhost."
    print "This system also assumes that you have run the specific graph_setup.py functions to build the Titan backend."

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
        elif action_to_do == 'all_people':
            with conn.transaction():
                people = conn.execute(QUERY_ALL_PEOPLE)
                for person in people:
                	print person.get('_properties')
            print 'Grabbed all the people vertices in the graph.'
    except Exception as e:
        print "Error occurred while attempting RexPro transactions."
        print str(e)
        sys.exit(2)

if __name__ == "__main__":
    main(sys.argv[1:])
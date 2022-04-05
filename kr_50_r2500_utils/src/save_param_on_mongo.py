#!/usr/bin/env python3

import pymongo
import pprint
import rospy

from std_msgs.msg import String
from pymongo import MongoClient

client = MongoClient('localhost', 27017)

db_param = rospy.get_param("/collection_name")
print(db_param)
db = client[db_param]

exec_collection       = db.exec_param
policy_collection     = db.policy_param
arbitrator_collection = db.arbitrator_param
learning_collection   = db.learning_param

if __name__ == '__main__':
	rospy.init_node('prova', anonymous=True)

	exec_params = rospy.get_param("/exec_params_mongo")

	if exec_param:
		exec_params_mongo = []
			for key_1 in exec_params.keys():
				for key_2 in exec_params[key_1].keys():
					data = exec_params[key_1][key_2]
					data["skill_type"] = key_1
					data["skill_name"] = key_2
					print(data)
					exec_params_mongo.append(data)

	exec_collection.delete_many({})
	exec_collection.insert_many(exec_params_mongo)

	# policy_collection.delete_many({})
	# policy_param = rospy.get_param("/policy_params_mongo")
	# policy_collection.insert_many(policy_param)
	#
	# arbitrator_collection.delete_many({})
	# arbitrator_param = rospy.get_param("/arbitrator_param_mongo")
	# arbitrator_collection.insert_many(arbitrator_param)
	#
	# learning_collection.delete_many({})
	# learning_param = rospy.get_param("/learning_param_mongo")
	# learning_collection.insert_many(learning_param)

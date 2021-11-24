"""
@Author: Samarth BM
@Date: 2021-11-23
@Last Modified by: Samarth BM
@Title : Program Aim perform hashtag count using pyflink
"""

import os
import random
from pyflink.table import (EnvironmentSettings, TableEnvironment, TableDescriptor, Schema,
                           DataTypes)
from pyflink.table.expressions import lit

 
# creating config
settings = EnvironmentSettings.new_instance().in_batch_mode().use_blink_planner().build()
t_env = TableEnvironment.create(settings)


def hashtag_count():
        
        try:
                input_file = '/home/samarth/Data-Engg/Flink/HashtagCounts/inputs.txt'
                output_file = '/home/samarth/Data-Engg/Flink/HashtagCounts/output'  
                # remove the output file, if there is one there already
                if os.path.isfile(output_file):
                        os.remove(output_file)
        
                # To generate input file with hashtags.
                hashtags = ['#virat', '#Rohit', '#Rahul', '#MSD']
                num_tweets = 1500
                with open(input_file, 'w') as f:
                        for tweet in range(num_tweets):
                                f.write('%s\n' % (random.choice(hashtags)))

                # write all the data to one file
                t_env.get_config().get_configuration().set_string("parallelism.default", "1")

                t_env.create_temporary_table(
                        'source',
                TableDescriptor.for_connector('filesystem')
                        .schema(Schema.new_builder()
                        .column('word', DataTypes.STRING())
                        .build())
                        .option('path', input_file)
                        .format('csv')
                        .build())
                tab = t_env.from_path('source')

                # doing transformation
                t_env.create_temporary_table(
                        'sink',
                TableDescriptor.for_connector('filesystem')
                        .schema(Schema.new_builder()
                        .column('word', DataTypes.STRING())
                        .column('count', DataTypes.BIGINT())
                        .build())
                        .option('path', output_file)
                        .format('csv')          
                        .build())
                        
                tab = t_env.from_path('source')
                tab.group_by(tab.word) \
                .select(tab.word, lit(1).count) \
                .execute_insert('sink').wait()
        
        except Exception as e:
                print(e)

hashtag_count()
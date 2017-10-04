#!/usr/bin/env python
# print('ytpy_db_utils')

# def getNextSequence(db, name):
#    ret = db.counters.findAndModify(
#           {
#             query: { _id: name },
#             update: { $inc: { seq: 1 } },
#             new: true
#           }
#    )
#    return ret.seq

# class DateTimeSupportJSONEncoder(json.JSONEncoder):
#     def default(self, o):
#         if isinstance(o, datetime):
#             return o.isoformat()
#         return super(DateTimeSupportJSONEncoder, self).default(o)

class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data, ensure_ascii=False) # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)

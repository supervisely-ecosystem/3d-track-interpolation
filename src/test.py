import json
import sly_globals as g


def api_test():
    data = {"figures_ids": [56655589, 56655590, 56655621, 56655596],
            "dataset_id": 33090,
            "track_id": "hello_track!"}
    r = g.api.task.send_request(g.task_id, "interpolate_figures_ids", data=data)

    print(json.dumps(r, indent=4))


api_test()

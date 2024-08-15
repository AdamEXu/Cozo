# CozoDB Visualization for Code Changes
This is a vector search and visualization tool for code changes from GitHub commits. It is built on top of CozoDB, and uses sentence-transformers to generate 384-dimensional embeddings for code changes. You can then search for similar code changes to a given code change, and visualize the code changes in a 2D space using t-SNE and MatPlotLib.

There are three components: Data Preparation, Visualization, and Vector Search.

But first, install all nescessary dependencies from the `requirements.txt` file.

```bash
python -m pip install -r requirements.txt
```

Once you have installed the dependencies, you can proceed to the Data Preparation section.

## Data Preparation
First, you will need to prepare the `explanations.db` file. By running `schema.py`, the script will create the `explanations.db` file with the necessary schema.

```bash
python schema.py
```

Once the database is initialized, you can insert the data. Data should be populated into the `gh_data.json` JSON file. The JSON file should contain a list of dictionaries, where each dictionary represents a data point. Each dictionary should contain the following keys:
- `code`: The code change for the data point in diff format.
- `repo`: The repository the code change belongs to.
- `commit_id`: The commit ID of the code change.
- `file`: The file the code change is from.
- `commit_message`: The commit message for the code change.
- `llm_explanation`: An LLM generated explanation for the code change.

Additionally, there is a `documentation_data.json` for documentation storage. The keys are similar but it should contain the following keys:
- `code`: The code change for the data point in diff format.
- `documentation`: Textual documentation for the code change surrounding the code change.
- `documentation_url`: URL to the documentation for the code change.
- `language`: The programming language of the code change.
- `llm_explanation`: An LLM generated explanation for the code change.

A sample dictionary is shown below:
```json
{
  "code": "@@ -606,37 +606,42 @@\ncdef _TSObject convert_str_to_tsobject(str ts, tzinfo tz,\n        # equiv: datetime.today().replace(tzinfo=tz)\n        return convert_datetime_to_tsobject(dt, tz, nanos=0, reso=NPY_FR_us)\n    else:\n-        string_to_dts_failed = string_to_dts(\n-            ts, &dts, &out_bestunit, &out_local,\n-            &out_tzoffset, False\n-        )\n-        if not string_to_dts_failed:\n-            reso = get_supported_reso(out_bestunit)\n-            check_dts_bounds(&dts, reso)\n-            obj = _TSObject()\n-            obj.dts = dts\n-            obj.creso = reso\n-            ival = npy_datetimestruct_to_datetime(reso, &dts)\n-\n-            if out_local == 1:\n-                obj.tzinfo = timezone(timedelta(minutes=out_tzoffset))\n-                obj.value = tz_localize_to_utc_single(\n-                    ival, obj.tzinfo, ambiguous='raise', nonexistent=None, creso=reso\n-                )\n-                if tz is None:\n-                    check_overflows(obj, reso)\n-                    return obj\n-                _adjust_tsobject_tz_using_offset(obj, tz)\n-                return  obj\n-            else:\n-                if tz is not None:\n-                    # shift for _localize_tso\n-                    ival = tz_localize_to_utc_single(\n-                        ival, tz, ambiguous='raise', nonexistent=None, creso=reso\n+        if not dayfirst:  # GH 58859\n+            string_to_dts_failed = string_to_dts(\n+                ts, &dts, &out_bestunit, &out_local,\n+                &out_tzoffset, False\n+            )\n+            if not string_to_dts_failed:\n+                reso = get_supported_reso(out_bestunit)\n+                check_dts_bounds(&dts, reso)\n+                obj = _TSObject()\n+                obj.dts = dts\n+                obj.creso = reso\n+                ival = npy_datetimestruct_to_datetime(reso, &dts)\n+\n+                if out_local == 1:\n+                    obj.tzinfo = timezone(timedelta(minutes=out_tzoffset))\n+                    obj.value = tz_localize_to_utc_single(\n+                        ival,\n+                        obj.tzinfo,\n+                        ambiguous='raise',\n+                        nonexistent=None,\n+                        creso=reso,\n                    )\n-                obj.value = ival\n-                maybe_localize_tso(obj, tz, obj.creso)\n-                return obj\n+                    if tz is None:\n+                        check_overflows(obj, reso)\n+                        return obj\n+                    _adjust_tsobject_tz_using_offset(obj, tz)\n+                    return  obj\n+                else:\n+                    if tz is not None:\n+                        # shift for _localize_tso\n+                        ival = tz_localize_to_utc_single(\n+                            ival, tz, ambiguous='raise', nonexistent=None, creso=reso\n+                        )\n+                    obj.value = ival\n+                    maybe_localize_tso(obj, tz, obj.creso)\n+                    return obj\n\n        dt = parse_datetime_string(\n            ts,",
  "repo": "pandas-dev/pandas",
  "commit_id": "288af5f",
  "file": "pandas/_libs/tslibs/conversion.pyx",
  "commit_message": "Fix to_datetime not respecting dayfirst",
  "explanation": "Description: Corrects the behavior of the conversion function to respect the dayfirst parameter.\nReason: To ensure that the dayfirst parameter is correctly handled when converting strings to datetime objects.\nChanges: Added a conditional check to handle the dayfirst parameter and restructured the code to properly localize the datetime object based on the timezone.\nImpact: Resolves the issue where the dayfirst parameter was not being considered during string-to-datetime conversion, improving the accuracy of datetime localization."
}
```

After populating this JSON file, run `insert_data.py` to insert the data into the CozoDB database.

```bash
python insert_data.py
```

## Visualization 
To start the visualization process, run `visualization.py`. 

```bash
python visualization.py
```

By running `visualization.py`, the script will generate a visualization for each perplexity value from 0.5 to 51.0 in increments of 0.5 into the `visualizations/` folder in the following format:

```
visualization_perplexity_0.5.png
visualization_perplexity_1.png
visualization_perplexity_1.5.png
...
visualization_perplexity_5.5.png
visualization_perplexity_6.png
```

The visualization will be a scatter plot of the t-SNE embeddings of the data points with labels containing the code change for each data point like the one shown below:
![A scatter plot containing points for each code change.](./readme_images/vis_perplexity_5.0.png)

## Vector Search
To search for similar code changes to a given code change, run `search.py`. The script will prompt the user to input a code change in diff format. The script will then output the 3 most similar code changes to the input code change. As of now, the change to search for is hardcoded in the `gh_search.py` and `documentation_search.py` files.

```bash
python gh_search.py
python documentation_search.py
```

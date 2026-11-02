import subprocess
from pathlib import Path

import bpy

LABEL = "Save Share Copy"
CATEGORY = "Export"
TOOLTIP = "Write <name>_share.blend beside the saved file with all linked data made local and external files packed; overwrite existing copy"
ORDER = 30

# Runs in a background Blender on the saved file, so the open file keeps its links
SHARE_SCRIPT = """
import sys
import bpy

if bpy.context.mode != 'OBJECT':
    bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.object.make_local(type='ALL')
bpy.data.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)
bpy.ops.file.pack_all()
bpy.ops.wm.save_as_mainfile(filepath=sys.argv[-1])

for id in bpy.data.user_map():
    if id.library:
        print("SHARE: still linked:", type(id).__name__, id.name)
for collection in (bpy.data.images, bpy.data.sounds, bpy.data.fonts, bpy.data.movieclips, bpy.data.cache_files, bpy.data.volumes):
    for id in collection:
        if id.filepath and id.filepath != "<builtin>" and not getattr(id, "packed_file", None):
            print("SHARE: not packed:", type(id).__name__, id.name, id.filepath)
"""


def run(context):
    if not bpy.data.filepath:
        raise ValueError("Save the file first")
    if bpy.data.is_dirty:
        raise ValueError("Save your changes first, the copy is made from the file on disk")
    source = Path(bpy.data.filepath)
    target = source.with_name(source.stem + "_share.blend")

    result = subprocess.run(
        [bpy.app.binary_path, "--background", "--factory-startup", str(source),
         "--python-exit-code", "1", "--python-expr", SHARE_SCRIPT, "--", str(target)],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        print(result.stdout, result.stderr)
        raise RuntimeError("Background Blender failed, see the console")

    problems = [line for line in result.stdout.splitlines() if line.startswith("SHARE:")]
    for line in problems:
        print(line)
    if problems:
        return f"Saved {target.name} with {len(problems)} problems, see the console"
    return f"Saved {target.name}"

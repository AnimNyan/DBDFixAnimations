# ##### BEGIN CC0 LICENSE BLOCK #####
#
# CC0 is a public domain dedication from Creative Commons. A work released under CC0 is 
# dedicated to the public domain to the fullest extent permitted by law. If that is not 
# possible for any reason, CC0 also provides a simple permissive license as a fallback. 
# Both public domain works and the simple license provided by CC0 are compatible with the GNU GPL.
#
#  You should have received a copy of the Creative Commons Zero Licence
#
# ##### END CC0 LICENSE BLOCK #####

# by Pan and Anime Nyan

from . import DBDFixAnimations

bl_info = {
    "name": "PSK/PSA DBD Fix Animations",
    "author": "Pan, Anime Nyan",
    "version": (1, 0, 6),
    "blender": (2, 93, 0),
    "location": "3D View > Properties > PSK PSA",
    "description": "Addon for befzz's 280 psk/psa importer add on to fix Dead By Daylight Animations",
    "warning": "",
    "wiki_url": "https://github.com/AnimNyan/DBDFixAnimations",
    "category": "Animation",
    "tracker_url": "https://github.com/AnimNyan/DBDFixAnimations"
}

def register():
    DBDFixAnimations.register()

def unregister():
    DBDFixAnimations.unregister()

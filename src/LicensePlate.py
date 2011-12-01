from xml.dom.minidom import parse 
from Error import Error
from Point import Point
from Character import Character

class LicensePlate:

    def __init__(self, file_path):
        try:
            self.dom = parse(file_path)
        except IOError:
            Error("Incorrect file name given.")
            return None
        else:
            properties = self.get_properties()

            self.image  = str(properties['uii']) + '.' + str(properties['type'])
            self.width  = properties['width']
            self.height = properties['height']

            info = self.set_plate()

    def get_properties(self):
        children = self.get_children("properties")

        properties = {}

        for child in children:
            if child.nodeType == child.TEXT_NODE:
                properties[child.nodeName] = child.data
            elif child.nodeType == child.ELEMENT_NODE:
                properties[child.nodeName] = child.firstChild.data

        return properties

    # TODO : create function for location / characters as they do the same
    def set_plate(self):
        children = self.get_children("plate") # most recent version
        
        for child in children:
            if child.nodeName == "regnum":
              self.license_full = child.firstChild.data
            elif child.nodeName == "identification-letters":
              self.country = child.firstChild.data
            elif child.nodeName == "location":
                corners = self.get_children("quadrangle", child)
          
                self.corners = []

                for corner in corners:
                  if corner.nodeName == "point":
                      self.corners.append(Point(corner))

            elif child.nodeName == "characters":
                characters = child.childNodes
  
                self.license_characters = []

                for character in characters:
                  if character.nodeName == "character":
                    self.license_characters.append(Character(character))

            else:
                pass
                #print child.nodeName
            
    def get_node(self, node, dom=None):
        if not dom:
            dom = self.dom

        return dom.getElementsByTagName(node)[0]

    def get_children(self, node, dom=None):
        return self.get_node(node, dom).childNodes
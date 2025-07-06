class EntityMediator:
    def __init__(self):
        self.groups = {}

    def register_group(self, name, group):
        self.groups[name] = group

    def collide(self, grp1, grp2, callback=None):
        for s1 in self.groups[grp1]:
            for s2 in self.groups[grp2]:
                if s1.rect.colliderect(s2.rect):
                    if callback:
                        callback(s1, s2)
from __future__ import annotations

class PermissionError(Exception):
    pass

class PermissionCode(int):
    OWNED         = 0b00001
    READ          = 0b00010
    WRITE         = 0b00100
    SHARE_READ    = 0b01000
    SHARE_WRITE   = 0b10000

    ALL           = 0b11111
    SHARE_MASK    = 0b11000
    SELF_MASK     = 0b00110
    SHARE_TO_SHIFT = 2

    PERMISSION_LIST = [(OWNED, 'owned'),    \
                        (READ, 'read'), (WRITE, 'write'),
                        (SHARE_READ, 'share_read'), (SHARE_WRITE, 'share_write')]

    def __str__(self) -> str:
        ret_str = ''
        for p in PermissionCode.PERMISSION_LIST:
            if self.is_contained(p[0]):
                ret_str += p[1] + ' '

        return f"{self:05b}:" + ret_str

    def share_permission(self) -> PermissionCode:
        return PermissionCode(self & PermissionCode.SHARE_MASK)
    
    def self_permission(self) -> PermissionCode:
        return PermissionCode(self & PermissionCode.SELF_MASK)

    def share_to_self(self) -> PermissionCode:
        return PermissionCode(self.share_permission() >> PermissionCode.SHARE_TO_SHIFT)

    def self_to_share(self) -> PermissionCode:
        return PermissionCode(self.self_permission() << PermissionCode.SHARE_TO_SHIFT)

    def is_contained(self, permissionCode: PermissionCode | int) -> bool:
        """return if self permission contains the provided permission"""
        return bool(self & permissionCode)


class Permission():
    data: PermissionCode

    def __init__(self, code: PermissionCode):
        if self.check(code):
            self.data = code
        else:
            raise ValueError("permission provided is illegal")

    def __str__(self) -> str:
        return f"Permission:({self.data})"

    def check(self, code: PermissionCode) -> bool:
        return True # TODO:

    def is_readable(self) -> bool:
        return self.data.is_contained(PermissionCode.READ)

    def is_writeable(self) -> bool:
        return self.data.is_contained(PermissionCode.WRITE)

    def max_share(self) -> Permission:
        share_p = self.data.share_permission()
        new_p = PermissionCode(share_p.share_to_self() + share_p)
        return Permission(new_p)


class PermissionFactory():

    @classmethod
    def readonly(cls) -> Permission:
        """can only read, not able to share
        """
        return Permission(PermissionCode(PermissionCode.READ))

    @classmethod
    def editable(cls) -> Permission:
        """can rw, also share rw
        """
        return Permission(PermissionCode(PermissionCode.READ | PermissionCode.WRITE | PermissionCode.SHARE_READ | PermissionCode.SHARE_WRITE))
    
    @classmethod
    def owner(cls) -> Permission:
        """permission all
        """
        return Permission(PermissionCode(PermissionCode.ALL))

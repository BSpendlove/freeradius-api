from loguru import logger
from sqlalchemy.orm import Session
from sqlalchemy.sql import exists
from typing import List

# Database Models
from ..models import (
    RadiusAccounting,
    RadiusCheck,
    RadiusGroupCheck,
    RadiusGroupReply,
    RadiusNAS,
    RadiusPostAuth,
    RadiusReply,
    RadiusUserGroup,
)

# Schemas (mainly for typehints)
from ..schemas import (
    RadiusAttribute,
    RadiusGroup,
    RadiusPostAuthentication,
    RadiusUser,
    RadiusUserAccounting,
)


def user_attributes(db: Session, user: RadiusUser) -> List[RadiusAttribute]:
    attributes = (
        db.query(RadiusCheck, RadiusGroupCheck)
        .filter(RadiusCheck.username == user.username)
        .filter(RadiusGroupCheck.username == user.username)
        .all()
    )
    return attributes


def user(db: Session, username: str) -> RadiusUser:
    user = (
        db.query(RadiusCheck)
        .with_entities(RadiusCheck.username)
        .filter(RadiusCheck.username == username)
        .first()
    )

    if user is None:
        check_if_in_groups = (
            db.query(RadiusUserGroup)
            .with_entities(RadiusUserGroup.username)
            .filter(RadiusUserGroup.username == username)
            .group_by(RadiusUserGroup.username)
            .first()
        )
        if check_if_in_groups is None:
            return

    user_radcheck_attributes = (
        db.query(RadiusCheck)
        .with_entities(
            RadiusCheck.id, RadiusCheck.attribute, RadiusCheck.op, RadiusCheck.value
        )
        .filter(RadiusCheck.username == username)
        .all()
    )

    user_radreply_attributes = (
        db.query(RadiusReply)
        .with_entities(
            RadiusReply.id, RadiusReply.attribute, RadiusReply.op, RadiusReply.value
        )
        .filter(RadiusReply.username == username)
        .all()
    )

    user_radgroups = (
        db.query(RadiusUserGroup)
        .with_entities(
            RadiusUserGroup.groupname,
            RadiusUserGroup.priority,
        )
        .filter(RadiusUserGroup.username == username)
        .all()
    )

    return RadiusUser(
        username=username,
        radcheck=user_radcheck_attributes,
        radreply=user_radreply_attributes,
        radusergroup=user_radgroups,
    )


def users(db: Session) -> List[RadiusUser]:
    users = (
        db.query(RadiusCheck)
        .with_entities(RadiusCheck.username)
        .group_by(RadiusCheck.username)
        .all()
    )

    stmt = exists().where(RadiusCheck.username == RadiusUserGroup.username)
    users_only_in_groups = (
        db.query(RadiusUserGroup)
        .with_entities(RadiusUserGroup.username)
        .group_by(RadiusUserGroup.username)
        .filter(~stmt)
    )

    if users_only_in_groups:
        users.extend(users_only_in_groups)

    users_and_attributes = []
    for user in users:
        user_radcheck_attributes = (
            db.query(RadiusCheck)
            .with_entities(
                RadiusCheck.id, RadiusCheck.attribute, RadiusCheck.op, RadiusCheck.value
            )
            .filter(RadiusCheck.username == user.username)
            .all()
        )

        user_radreply_attributes = (
            db.query(RadiusReply)
            .with_entities(
                RadiusReply.id, RadiusReply.attribute, RadiusReply.op, RadiusReply.value
            )
            .filter(RadiusReply.username == user.username)
            .all()
        )

        user_radgroups = (
            db.query(RadiusUserGroup)
            .with_entities(
                RadiusUserGroup.groupname,
                RadiusUserGroup.priority,
            )
            .filter(RadiusUserGroup.username == user.username)
            .all()
        )

        users_and_attributes.append(
            RadiusUser(
                username=user.username,
                radcheck=user_radcheck_attributes,
                radreply=user_radreply_attributes,
                radusergroup=user_radgroups,
            )
        )
    return users_and_attributes


def group(db: Session, groupname: str) -> RadiusGroup:
    group = (
        db.query(RadiusGroupCheck)
        .filter(RadiusGroupCheck.groupname == groupname)
        .first()
    )

    if group is None:
        return

    group_radcheck_attributes = (
        db.query(RadiusGroupCheck)
        .with_entities(
            RadiusGroupCheck.id,
            RadiusGroupCheck.attribute,
            RadiusGroupCheck.op,
            RadiusGroupCheck.value,
        )
        .filter(RadiusGroupCheck.groupname == group.groupname)
        .all()
    )

    group_radreply_attributes = (
        db.query(RadiusGroupReply)
        .with_entities(
            RadiusGroupReply.id,
            RadiusGroupReply.attribute,
            RadiusGroupReply.op,
            RadiusGroupReply.value,
        )
        .filter(RadiusGroupReply.groupname == group.groupname)
        .all()
    )

    group_radgroupusers = (
        db.query(RadiusUserGroup)
        .with_entities(RadiusUserGroup.username)
        .filter(RadiusUserGroup.groupname == group.groupname)
        .group_by(RadiusUserGroup.username)
        .all()
    )

    return RadiusGroup(
        groupname=group.groupname,
        radgroupcheck=group_radcheck_attributes,
        radgroupreply=group_radreply_attributes,
        radusergroup=group_radgroupusers,
    )


def group_check_attributes(db: Session, groupname: str) -> List[RadiusAttribute]:
    attributes = (
        db.query(RadiusGroupCheck).filter(RadiusGroupCheck.groupname == groupname).all()
    )
    return attributes


def group_reply_attributes(db: Session, groupname: str) -> List[RadiusAttribute]:
    attributes = (
        db.query(RadiusGroupReply).filter(RadiusGroupReply.groupname == groupname).all()
    )
    return attributes


def groups(db: Session) -> List[RadiusGroup]:
    groups = db.query(RadiusGroupCheck).group_by(RadiusGroupCheck.groupname).all()

    groups_and_attributes = []
    for group in groups:
        group_radcheck_attributes = (
            db.query(RadiusGroupCheck)
            .with_entities(
                RadiusGroupCheck.id,
                RadiusGroupCheck.attribute,
                RadiusGroupCheck.op,
                RadiusGroupCheck.value,
            )
            .filter(RadiusGroupCheck.groupname == group.groupname)
            .all()
        )

        group_radreply_attributes = (
            db.query(RadiusGroupReply)
            .with_entities(
                RadiusGroupReply.id,
                RadiusGroupReply.attribute,
                RadiusGroupReply.op,
                RadiusGroupReply.value,
            )
            .filter(RadiusGroupReply.groupname == group.groupname)
            .all()
        )

        group_radgroupusers = (
            db.query(RadiusUserGroup)
            .with_entities(RadiusUserGroup.username)
            .filter(RadiusUserGroup.groupname == group.groupname)
            .group_by(RadiusUserGroup.username)
            .all()
        )

        groups_and_attributes.append(
            RadiusGroup(
                groupname=group.groupname,
                radgroupcheck=group_radcheck_attributes,
                radgroupreply=group_radreply_attributes,
                radusergroup=group_radgroupusers,
            )
        )

    return groups_and_attributes


def postauth(
    db: Session, skip: int = 0, limit: int = 100
) -> List[RadiusPostAuthentication]:
    postauth_data = (
        db.query(RadiusPostAuth)
        .order_by(RadiusPostAuth.id.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return postauth_data


def postauth_user(
    db: Session, username: str, skip: int = 0, limit: int = 100
) -> List[RadiusPostAuthentication]:
    postauth_data = (
        db.query(RadiusPostAuth)
        .filter(RadiusPostAuth.username == username)
        .order_by(RadiusPostAuth.id.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return postauth_data


def accounting(
    db: Session, skip: int = 0, limit: int = 100
) -> List[RadiusUserAccounting]:
    accounting_data = (
        db.query(RadiusAccounting)
        .order_by(RadiusAccounting.radacctid.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return accounting_data


def accounting_user(
    db: Session, username: str, skip: int = 0, limit: int = 100
) -> List[RadiusUserAccounting]:
    accounting_data = (
        db.query(RadiusAccounting)
        .filter(RadiusAccounting.username == username)
        .order_by(RadiusAccounting.radacctid.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return accounting_data

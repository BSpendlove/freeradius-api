from loguru import logger
from sqlalchemy.orm import Session
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
    RadiusUser,
    RadiusUserCreate,
    RadiusGroupCreate,
)
from .read import user as read_user
from .read import group as read_group


def user(db: Session, user: RadiusUserCreate) -> RadiusUser:
    radusergroup = RadiusUserGroup(groupname=user.groupname, username=user.username)
    if user.password:
        user_radcheck = RadiusCheck(
            username=user.username,
            attribute="Cleartext-Password",
            op=":=",
            value=user.password,
        )
        db.add_all(radusergroup, user_radcheck)
    else:
        db.add(radusergroup)

    try:
        db.commit()
        logger.info(f"Created User ({user.username})")
    except:
        db.rollback()
        logger.error(f"Unable to create User ({user.username})")
        return

    return read_user(db=db, username=user.username)


def user_check_attribute(
    db: Session, user: RadiusUser, attribute: RadiusAttribute
) -> RadiusUser:
    check_avpair = RadiusCheck(
        username=user.username,
        attribute=attribute.attribute,
        op=attribute.op,
        value=attribute.value,
    )

    db.add(check_avpair)
    try:
        db.commit()
        logger.info(
            f"Adding User {user.username} RadCheck Attribute ({attribute.attribute} {attribute.op} {attribute.value})"
        )
    except:
        db.rollback()
        logger.error(f"Unable to add RadCheck Attribute for User {user.username}")
        return

    return read_user(db=db, username=user.username)


def user_reply_attribute(
    db: Session, user: RadiusUser, attribute: RadiusAttribute
) -> RadiusUser:
    reply_avpair = RadiusReply(
        username=user.username,
        attribute=attribute.attribute,
        op=attribute.op,
        value=attribute.value,
    )

    db.add(reply_avpair)
    try:
        db.commit()
        logger.info(
            f"Adding User {user.username} RadReply Attribute ({attribute.attribute} {attribute.op} {attribute.value})"
        )
    except:
        db.rollback()
        logger.error(f"Unable to add RadCheck Attribute for User {user.username}")
        return

    return read_user(db=db, username=user.username)


def group(db: Session, group: RadiusGroupCreate) -> RadiusGroup:
    radgroupcheck = RadiusGroupCheck(
        groupname=group.groupname,
        attribute="Cleartext-Password",
        op=":=",
        value=group.password,
    )

    db.add(radgroupcheck)
    try:
        db.commit()
        logger.info(f"Created Group ({group.groupname})")
    except:
        db.rollback()
        logger.error(f"Unable to create Group ({group.groupname})")
        return

    return read_group(db=db, groupname=group.groupname)


def group_check_attribute(
    db: Session, group: RadiusGroup, attribute: RadiusAttribute
) -> RadiusGroup:
    check_avpair = RadiusGroupCheck(
        groupname=group.groupname,
        attribute=attribute.attribute,
        op=attribute.op,
        value=attribute.value,
    )

    db.add(check_avpair)
    try:
        db.commit()
        logger.info(
            f"Adding Group {group.groupname} RadGroupCheck Attribute ({attribute.attribute} {attribute.op} {attribute.value})"
        )
    except:
        db.rollback()
        logger.error(
            f"Unable to add GroupRadCheck Attribute for Group {group.groupname}"
        )
        return

    return read_group(db=db, groupname=group.groupname)


def group_reply_attribute(
    db: Session, group: RadiusGroup, attribute: RadiusAttribute
) -> RadiusGroup:
    reply_avpair = RadiusGroupReply(
        groupname=group.groupname,
        attribute=attribute.attribute,
        op=attribute.op,
        value=attribute.value,
    )

    db.add(reply_avpair)
    try:
        db.commit()
        logger.info(
            f"Adding Group {group.groupname} RadGroupReply Attribute ({attribute.attribute} {attribute.op} {attribute.value})"
        )
    except:
        db.rollback()
        logger.error(
            f"Unable to add GroupRadReply Attribute for Group {group.groupname}"
        )
        return

    return read_group(db=db, groupname=group.groupname)

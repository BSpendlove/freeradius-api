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
from ..schemas import RadiusAttribute, RadiusGroup, RadiusUser


def user(db: Session, username: str) -> int:
    deleted_rows = (
        db.query(RadiusCheck).filter(RadiusCheck.username == username).delete()
    )

    deleted_rows += (
        db.query(RadiusReply).filter(RadiusReply.username == username).delete()
    )

    deleted_rows += (
        db.query(RadiusUserGroup).filter(RadiusUserGroup.username == username).delete()
    )

    try:
        db.commit()
        logger.info(f"Deleted User {username} (deleted_rows: {deleted_rows})")
    except:
        db.rollback()
        logger.error(f"Unable to delete User {username}")
        return

    return deleted_rows


def user_check_attribute(
    db: Session, user: RadiusUser, attribute: RadiusAttribute
) -> RadiusUser:
    deleted_rows = (
        db.query(RadiusCheck)
        .filter(
            RadiusCheck.username == user.username,
            RadiusCheck.attribute == attribute.attribute,
            RadiusCheck.op == attribute.op,
            RadiusCheck.value == attribute.value,
        )
        .delete()
    )

    try:
        db.commit()
        logger.info(
            f"Deleted User {user.username} RadCheck Attribute ({attribute.attribute} {attribute.op} {attribute.value}) (deleted_rows: {deleted_rows})"
        )
    except:
        db.rollback()
        logger.error(f"Unable to delete User {user.username} RadCheck Attribute")
        return

    return deleted_rows


def user_reply_attribute(
    db: Session, user: RadiusUser, attribute: RadiusAttribute
) -> RadiusUser:
    deleted_rows = (
        db.query(RadiusReply)
        .filter(
            RadiusReply.username == user.username,
            RadiusReply.attribute == attribute.attribute,
            RadiusReply.op == attribute.op,
            RadiusReply.value == attribute.value,
        )
        .delete()
    )

    try:
        db.commit()
        logger.info(
            f"Deleted User {user.username} RadReply Attribute ({attribute.attribute} {attribute.op} {attribute.value}) (deleted_rows: {deleted_rows})"
        )
    except:
        db.rollback()
        logger.error(f"Unable to delete User {user.username} RadReply Attribute")
        return

    return deleted_rows


def group(db: Session, groupname: str) -> int:
    deleted_rows = (
        db.query(RadiusGroupCheck)
        .filter(RadiusGroupCheck.groupname == groupname)
        .delete()
    )

    deleted_rows += (
        db.query(RadiusGroupReply)
        .filter(RadiusGroupReply.groupname == groupname)
        .delete()
    )

    try:
        db.commit()
        logger.info(f"Deleted Group {groupname} (deleted_rows: {deleted_rows})")
    except:
        db.rollback()
        logger.error(f"Unable to delete Group {groupname}")
        return

    return deleted_rows


def group_check_attribute(
    db: Session, group: RadiusGroup, attribute: RadiusAttribute
) -> RadiusGroup:
    deleted_rows = (
        db.query(RadiusGroupCheck)
        .filter(
            RadiusGroupCheck.groupname == group.groupname,
            RadiusGroupCheck.attribute == attribute.attribute,
            RadiusGroupCheck.op == attribute.op,
            RadiusGroupCheck.value == attribute.value,
        )
        .delete()
    )

    try:
        db.commit()
        logger.info(
            f"Deleted Group {group.groupname} RadGroupCheck Attribute ({attribute.attribute} {attribute.op} {attribute.value}) (deleted_rows: {deleted_rows})"
        )
    except:
        db.rollback()
        logger.error(
            f"Unable to delete Group {group.groupname} RadGroupCheck Attribute"
        )
        return

    return deleted_rows


def group_reply_attribute(
    db: Session, group: RadiusGroup, attribute: RadiusAttribute
) -> RadiusGroup:
    deleted_rows = (
        db.query(RadiusGroupReply)
        .filter(
            RadiusGroupReply.groupname == group.groupname,
            RadiusGroupReply.attribute == attribute.attribute,
            RadiusGroupReply.op == attribute.op,
            RadiusGroupReply.value == attribute.value,
        )
        .delete()
    )

    try:
        db.commit()
        logger.info(
            f"Deleted Group {group.groupname} RadGroupReply Attribute ({attribute.attribute} {attribute.op} {attribute.value}) (deleted_rows: {deleted_rows})"
        )
    except:
        db.rollback()
        logger.error(
            f"Unable to delete Group {group.groupname} RadGroupReply Attribute"
        )
        return

    return deleted_rows


def postauth(db: Session) -> int:
    deleted_rows = db.query(RadiusPostAuth).delete()

    try:
        db.commit()
        logger.info(f"Deleted all PostAuth data (deleted_rows: {deleted_rows})")
    except:
        db.rollback()
        logger.error(f"Unable to delete all PostAuth data")
        return

    return deleted_rows


def postauth_user(db: Session, username: str) -> int:
    deleted_rows = (
        db.query(RadiusPostAuth).filter(RadiusPostAuth.username == username).delete()
    )

    try:
        db.commit()
        logger.info(
            f"Deleted PostAuth for User {username} (deleted_rows: {deleted_rows})"
        )
    except:
        db.rollback()
        logger.error(f"Unable to PostAuth for User {username}")
        return

    return deleted_rows


def accounting(db: Session) -> int:
    deleted_rows = db.query(RadiusAccounting).delete()

    try:
        db.commit()
        logger.info(f"Deleted all RadAcct data (deleted_rows: {deleted_rows})")
    except:
        db.rollback()
        logger.error(f"Unable to delete all RadAcct data")
        return

    return deleted_rows


def accounting_user(db: Session, username: str) -> int:
    deleted_rows = (
        db.query(RadiusAccounting)
        .filter(RadiusAccounting.username == username)
        .delete()
    )

    try:
        db.commit()
        logger.info(
            f"Deleted RadAcct for User {username} (deleted_rows: {deleted_rows})"
        )
    except:
        db.rollback()
        logger.error(f"Unable to RadAcct for User {username}")
        return

    return deleted_rows

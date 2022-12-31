--
-- radgroupcheck
--
LOCK TABLES `radgroupcheck` WRITE;
INSERT INTO `radgroupcheck` VALUES 
   (1,'SPEED_500','Cleartext-Password',':=','default'),
   (2,'SPEED_1000','Cleartext-Password',':=','default');
UNLOCK TABLES;

--
-- radgroupreply
--
LOCK TABLES `radgroupreply` WRITE;
INSERT INTO `radgroupreply` VALUES 
(1,'SPEED_1000','Cisco-AVPair','+=','subscriber:sub-qos-policy-in=PM_SPEED_1000'),
(2,'SPEED_1000','Cisco-AVPair','+=','subscriber:sub-qos-policy-in=PM_SPEED_1000'),
(3,'SPEED_STATIC','Fall-Through','=','yes'),
(4,'SPEED_STATIC','Cisco-AVPair','+=','ipv4-unnumbered=Loopback1000'),
(5,'SPEED_STATIC','Cisco-AVPair','+=','primary-dns=1.1.1.1'),
(6,'SPEED_STATIC','Cisco-AVPair','+=','secondary-dns=8.8.8.8'),
(7,'SPEED_STATIC','Cisco-AVPair','+=','vrf-id=VRF-STATIC');
UNLOCK TABLES;

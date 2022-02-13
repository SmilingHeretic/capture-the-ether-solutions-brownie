pragma solidity ^0.4.21;

contract ICaptureTheEther {
    function setNickname(bytes32 nickname) external;

    function nicknameOf(address) external view returns (bytes32);
}

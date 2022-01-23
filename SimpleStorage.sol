//SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SimpleStorage {
    // THIS WILL INITIALIZED AS ZERO
    uint256 public favoriteNumber;

    function store(uint256 _favoriteNumber) public {
        favoriteNumber = _favoriteNumber;
    }

    function retrieve() public view returns (uint256) {
        return favoriteNumber;
    }

    struct People {
        uint256 favoriteNumber;
        string name;
    }

    People public person = People({favoriteNumber: 345, name: "cat"});
    // WE CAN CREATE BOTH DYNAMIC AND FIXED(with People[1]) SIZE ARRAY
    People[] public people;
    mapping(string => uint256) public nameToFavoriteNumber;

    // ADD PEOPLE TO A DYNAMIC ARRAY
    function addPeople(string memory _name, uint256 _favoriteNumber) public {
        // storage PERSISTS VALUE EVEN AFTER THE FUNCTION IS RUN
        people.push(People({favoriteNumber: _favoriteNumber, name: _name}));
        nameToFavoriteNumber[_name] = _favoriteNumber;
    }
}

import React, { useEffect, useState } from "react";

interface ImageWithIdProps {
  id: number;
  url: string;
  selected?: boolean;
  onSelect?: (id: number, selected: boolean) => void;
}

const ImageWithId: React.FC<ImageWithIdProps> = ({ id, url, selected = false, onSelect }) => {

  const handleClick = () => {
    if (onSelect) onSelect(id, !selected);
  };

  return (
    <div
      onClick={handleClick}
      style={{
        position: "relative",
        display: "inline-block",
        margin: "10px",
        cursor: "pointer",
        border: selected ? "4px solid #00f" : "4px solid transparent",
        borderRadius: "8px",
        transition: "border 0.2s",
      }}
    >
      <img
        src={url}
        alt={`img-${id}`}
        style={{
          width: "200px",
          borderRadius: "8px",
          display: "block",
          opacity: selected ? 0.8 : 1,
          transition: "opacity 0.2s",
        }}
      />
      <div
        style={{
          position: "absolute",
          top: "5px",
          right: "5px",
          backgroundColor: "rgba(0,0,0,0.7)",
          color: "white",
          padding: "4px 8px",
          borderRadius: "6px",
          fontSize: "14px",
          fontWeight: "bold",
        }}
      >
        {id}
      </div>
    </div>
  );
};

export default ImageWithId;
